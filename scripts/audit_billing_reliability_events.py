#!/usr/bin/env python3
"""Audit local billing-reliability CTA event coverage.

This is a static guardrail for the revenue funnel. It does not call PostHog or
claim real traffic; it checks that revenue-critical pages expose the event names
and CTA metadata needed for later analytics.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


SITE_ROOT = Path("/home/openclaw/goosekit.dev")


@dataclass(frozen=True)
class RequiredEvent:
    path: str
    event: str
    location: str | None = None
    product: str | None = "billing_reliability"
    needs_score_attrs: bool = False
    require_product: bool = False


@dataclass(frozen=True)
class RequiredLink:
    path: str
    href: str
    label: str


REQUIRED_EVENTS = [
    RequiredEvent("/stripe-supabase-billing-drift-check/", "billing_drift_review_request", "drift_check_result", needs_score_attrs=True, require_product=True),
    RequiredEvent("/stripe-supabase-billing-drift-check/", "setup_help_retainer_interest", "drift_check_result", needs_score_attrs=True, require_product=True),
    RequiredEvent("/stripe-supabase-billing-drift-check/", "setup_help_secondary_clicked", "drift_check_bottom", require_product=True),
    RequiredEvent("/stripe-supabase-billing-drift-check/", "billing_drift_check_secondary", "drift_check_bottom", require_product=True),
    RequiredEvent("/stripe-billing-reliability-checklist/", "billing_drift_check_clicked", "billing_reliability_checklist_top", require_product=True),
    RequiredEvent("/stripe-billing-reliability-checklist/", "setup_help_retainer_interest", "billing_reliability_checklist_top", require_product=True),
    RequiredEvent("/stripe-billing-reliability-checklist/", "billing_drift_check_clicked", "billing_reliability_checklist_bottom", require_product=True),
    RequiredEvent("/stripe-billing-reliability-checklist/", "setup_help_retainer_interest", "billing_reliability_checklist_bottom", require_product=True),
    RequiredEvent("/stripe-billing-reliability-checklist/", "setup_help_secondary_clicked", "billing_reliability_checklist_bottom", require_product=True),
    RequiredEvent("/stripe-billing-reliability-checklist/", "billing_reliability_evidence_packet", "billing_reliability_evidence_packet", require_product=True),
    RequiredEvent("/stripe-billing-reliability-checklist/", "revenue_leak_audit_interest", "billing_reliability_evidence_packet", require_product=True),
    RequiredEvent("/stripe-supabase-revenue-leak-audit/", "revenue_leak_audit_request_clicked", "revenue_leak_evidence_packet", require_product=True),
    RequiredEvent("/stripe-supabase-revenue-leak-audit/", "billing_drift_check_clicked", "revenue_leak_evidence_packet", require_product=True),
    RequiredEvent("/stripe-supabase-revenue-leak-audit/", "setup_help_retainer_interest", "revenue_leak_audit_bottom", require_product=True),
    RequiredEvent("/stripe-supabase-revenue-leak-audit/", "setup_help_secondary_clicked", "revenue_leak_audit_bottom", require_product=True),
    RequiredEvent("/billing-health-support/", "billing_health_interest", "billing_health_hero"),
    RequiredEvent("/billing-health-support/", "billing_health_secondary_clicked", "billing_health_live_money_gate"),
    RequiredEvent("/nextjs-supabase-stripe-setup-help/", "setup_help_request_clicked", "live_money_gate_block"),
    RequiredEvent("/nextjs-supabase-stripe-setup-help/", "setup_help_retainer_interest", "retainer_block", require_product=True),
    RequiredEvent("/nextjs-supabase-stripe-setup-help/", "setup_help_retainer_interest", "setup_help_artifacts_monthly_support", require_product=True),
    RequiredEvent("/ship-it-kit-setup-help/", "setup_help_request_clicked", "shipit_setup_help_hero_packet"),
    RequiredEvent("/ship-it-kit-setup-help/", "setup_help_request_clicked", "shipit_setup_help_packet"),
    RequiredEvent("/ship-it-kit-setup-help/", "ship_it_kit_setup_help_clicked", "bottom_email_fallback"),
    RequiredEvent("/ship-it-kit-setup-help/", "billing_health_interest", "shipit_setup_help_hero_retainer"),
    RequiredEvent("/blog/stripe-webhook-supabase-paid-status/", "billing_drift_check_clicked", "webhook_paid_status_top"),
    RequiredEvent("/blog/stripe-webhook-duplicate-events-idempotency-supabase/", "billing_drift_check_clicked", "duplicate_webhook_top", require_product=True),
    RequiredEvent("/blog/stripe-webhook-duplicate-events-idempotency-supabase/", "setup_help_request_clicked", "duplicate_webhook_23505_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-webhook-event-ordering-supabase/", "billing_drift_check_clicked", "event_ordering_top"),
    RequiredEvent("/blog/stripe-trial-ending-supabase-access/", "billing_drift_check_clicked", "trial_top"),
    RequiredEvent("/blog/stripe-dunning-past-due-unpaid-supabase-access/", "billing_drift_check_clicked", "dunning_top"),
    RequiredEvent("/blog/stripe-customer-portal-cancel-supabase-status/", "billing_drift_check_clicked", "portal_cancel_top"),
    RequiredEvent("/blog/stripe-customer-portal-plan-change-supabase-entitlements/", "billing_drift_check_clicked", "portal_plan_change_top"),
    RequiredEvent("/blog/stripe-charged-customer-not-provisioned-supabase/", "billing_drift_check_clicked", "charged_stranded_top"),
    RequiredEvent("/blog/stripe-duplicate-subscription-supabase-access/", "billing_drift_check_clicked", "duplicate_subscription_top"),
    RequiredEvent("/blog/stripe-invoice-paid-double-extends-supabase-membership/", "billing_drift_check_clicked", "invoice_paid_double_extend_top"),
    RequiredEvent("/blog/stripe-invoice-paid-double-extends-supabase-membership/", "setup_help_request_clicked", "invoice_paid_double_extend_bottom_mailto"),
    RequiredEvent("/blog/stripe-client-paid-flag-supabase-bypass/", "billing_drift_check_clicked", "paid_flag_bypass_top"),
    RequiredEvent("/blog/stripe-client-paid-flag-supabase-bypass/", "setup_help_request_clicked", "paid_flag_bypass_bottom_mailto"),
    RequiredEvent("/blog/saas-credits-deducted-job-failed-no-refund/", "billing_drift_check_clicked", "metered_credit_job_failed_top", require_product=True),
    RequiredEvent("/blog/saas-credits-deducted-job-failed-no-refund/", "setup_help_request_clicked", "metered_credit_job_failed_bottom_mailto", require_product=True),
    RequiredEvent("/blog/saas-credits-deducted-job-failed-no-refund/", "revenue_leak_audit_interest", "metered_credit_job_failed_bottom", require_product=True),
    RequiredEvent("/blog/stripe-checkout-success-url-webhook-access/", "billing_drift_check_clicked", "checkout_success_webhook_top", require_product=True),
    RequiredEvent("/blog/stripe-checkout-success-url-webhook-access/", "setup_help_request_clicked", "checkout_success_webhook_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-checkout-success-url-webhook-access/", "setup_help_secondary_clicked", "checkout_success_webhook_related", require_product=True),
    RequiredEvent("/blog/stripe-setup-mode-card-on-file-subscription-gate/", "billing_drift_check_clicked", "setup_mode_card_gate_top", require_product=True),
    RequiredEvent("/blog/stripe-setup-mode-card-on-file-subscription-gate/", "setup_help_request_clicked", "setup_mode_card_gate_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-setup-mode-card-on-file-subscription-gate/", "setup_help_secondary_clicked", "setup_mode_card_gate_related", require_product=True),
    RequiredEvent("/blog/stripe-subscription-monthly-credits-double-grant-supabase/", "billing_drift_check_clicked", "monthly_credit_grant_top", require_product=True),
    RequiredEvent("/blog/stripe-subscription-monthly-credits-double-grant-supabase/", "setup_help_request_clicked", "monthly_credit_refill_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-subscription-monthly-credits-double-grant-supabase/", "setup_help_secondary_clicked", "monthly_credit_grant_related", require_product=True),
    RequiredEvent("/blog/stripe-subscription-add-credit-checkout-ledger/", "billing_drift_check_clicked", "subscription_add_credit_top", require_product=True),
    RequiredEvent("/blog/stripe-subscription-add-credit-checkout-ledger/", "setup_help_secondary_clicked", "subscription_add_credit_packet_jump", require_product=True),
    RequiredEvent("/blog/stripe-subscription-add-credit-checkout-ledger/", "setup_help_request_clicked", "subscription_add_credit_packet_mailto", require_product=True),
    RequiredEvent("/blog/stripe-subscription-add-credit-checkout-ledger/", "setup_help_request_clicked", "subscription_add_credit_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-subscription-add-credit-checkout-ledger/", "setup_help_secondary_clicked", "subscription_add_credit_related", require_product=True),
    RequiredEvent("/blog/stripe-hosted-plan-entitlement-provisioning-supabase/", "billing_drift_check_clicked", "hosted_plan_entitlement_top", require_product=True),
    RequiredEvent("/blog/stripe-hosted-plan-entitlement-provisioning-supabase/", "setup_help_request_clicked", "hosted_plan_entitlement_packet_mailto", require_product=True),
    RequiredEvent("/blog/stripe-hosted-plan-entitlement-provisioning-supabase/", "setup_help_request_clicked", "hosted_plan_entitlement_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-hosted-plan-entitlement-provisioning-supabase/", "setup_help_secondary_clicked", "hosted_plan_entitlement_related", require_product=True),
    RequiredEvent("/blog/stripe-connect-transfer-reversed-clawback-ledger/", "billing_drift_check_clicked", "connect_transfer_reversal_top", require_product=True),
    RequiredEvent("/blog/stripe-connect-transfer-reversed-clawback-ledger/", "revenue_leak_audit_interest", "connect_transfer_reversal_top", require_product=True),
    RequiredEvent("/blog/stripe-connect-transfer-reversed-clawback-ledger/", "setup_help_request_clicked", "connect_transfer_reversal_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-connect-transfer-reversed-clawback-ledger/", "setup_help_secondary_clicked", "connect_transfer_reversal_related", require_product=True),
    RequiredEvent("/blog/stripe-connect-affiliate-revenue-share-ledger/", "billing_drift_check_clicked", "affiliate_revenue_share_top", require_product=True),
    RequiredEvent("/blog/stripe-connect-affiliate-revenue-share-ledger/", "revenue_leak_audit_interest", "affiliate_revenue_share_top", require_product=True),
    RequiredEvent("/blog/stripe-connect-affiliate-revenue-share-ledger/", "setup_help_request_clicked", "affiliate_revenue_share_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-connect-affiliate-revenue-share-ledger/", "setup_help_secondary_clicked", "affiliate_revenue_share_related", require_product=True),
    RequiredEvent("/blog/stripe-course-membership-supabase-access/", "billing_drift_check_clicked", "course_membership_top", require_product=True),
    RequiredEvent("/blog/stripe-course-membership-supabase-access/", "setup_help_request_clicked", "course_membership_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-course-membership-supabase-access/", "setup_help_retainer_interest", "course_membership_bottom", require_product=True),
    RequiredEvent("/blog/stripe-course-membership-supabase-access/", "setup_help_secondary_clicked", "course_membership_related", require_product=True),
    RequiredEvent("/blog/stripe-zalopay-revenuecat-supabase-subscriptions/", "billing_drift_check_clicked", "multi_provider_subscription_top", require_product=True),
    RequiredEvent("/blog/stripe-zalopay-revenuecat-supabase-subscriptions/", "setup_help_request_clicked", "multi_provider_subscription_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-zalopay-revenuecat-supabase-subscriptions/", "setup_help_retainer_interest", "multi_provider_subscription_bottom", require_product=True),
    RequiredEvent("/blog/stripe-zalopay-revenuecat-supabase-subscriptions/", "setup_help_secondary_clicked", "multi_provider_subscription_related", require_product=True),
    RequiredEvent("/blog/stripe-prepaid-invoice-account-credit-ledger/", "billing_drift_check_clicked", "prepaid_credit_top", require_product=True),
    RequiredEvent("/blog/stripe-prepaid-invoice-account-credit-ledger/", "revenue_leak_audit_interest", "prepaid_credit_top", require_product=True),
    RequiredEvent("/blog/stripe-prepaid-invoice-account-credit-ledger/", "setup_help_request_clicked", "prepaid_credit_bottom_mailto", require_product=True),
    RequiredEvent("/blog/stripe-prepaid-invoice-account-credit-ledger/", "setup_help_retainer_interest", "prepaid_credit_bottom", require_product=True),
    RequiredEvent("/blog/stripe-prepaid-invoice-account-credit-ledger/", "setup_help_secondary_clicked", "prepaid_credit_related", require_product=True),
]

REQUIRED_LINKS = [
    RequiredLink(
        "/blog/stripe-webhook-supabase-paid-status/",
        "/blog/stripe-checkout-success-url-webhook-access/?ref=webhook_paid_status_success_url",
        "paid-status success URL contextual link",
    ),
    RequiredLink(
        "/blog/stripe-webhook-supabase-paid-status/",
        "/blog/stripe-checkout-success-url-webhook-access/?ref=webhook_paid_status_bottom",
        "paid-status bottom success URL CTA",
    ),
    RequiredLink(
        "/blog/stripe-webhook-signature-verification-failed-production/",
        "/blog/stripe-checkout-success-url-webhook-access/?ref=webhook_signature_success_url",
        "signature success URL contextual link",
    ),
    RequiredLink(
        "/blog/stripe-webhook-signature-verification-failed-production/",
        "/blog/stripe-checkout-success-url-webhook-access/?ref=webhook_signature_bottom",
        "signature bottom success URL CTA",
    ),
    RequiredLink(
        "/blog/stripe-webhook-duplicate-events-idempotency-supabase/",
        "/blog/stripe-checkout-success-url-webhook-access/?ref=duplicate_webhook_bottom",
        "duplicate webhook bottom success URL CTA",
    ),
    RequiredLink(
        "/blog/stripe-webhook-duplicate-events-idempotency-supabase/",
        "/blog/stripe-checkout-success-url-webhook-access/?ref=duplicate_webhook_related_list",
        "duplicate webhook related success URL link",
    ),
    RequiredLink(
        "/blog/stripe-trial-ending-supabase-access/",
        "/blog/stripe-setup-mode-card-on-file-subscription-gate/?ref=trial_setup_mode_context",
        "trial setup-mode contextual link",
    ),
    RequiredLink(
        "/blog/stripe-trial-ending-supabase-access/",
        "/blog/stripe-setup-mode-card-on-file-subscription-gate/?ref=trial_bottom_setup_mode",
        "trial bottom setup-mode CTA",
    ),
    RequiredLink(
        "/blog/stripe-checkout-success-url-webhook-access/",
        "/blog/stripe-setup-mode-card-on-file-subscription-gate/?ref=checkout_success_setup_mode_context",
        "checkout success setup-mode contextual link",
    ),
    RequiredLink(
        "/blog/stripe-checkout-success-url-webhook-access/",
        "/blog/stripe-setup-mode-card-on-file-subscription-gate/?ref=checkout_success_bottom_setup_mode",
        "checkout success bottom setup-mode CTA",
    ),
    RequiredLink(
        "/stripe-supabase-revenue-leak-audit/",
        "/go/billing-reliability/audit-request/?source=revenue_leak_audit_cta",
        "revenue leak audit tracked request route",
    ),
    RequiredLink(
        "/stripe-supabase-revenue-leak-audit/",
        "/go/billing-reliability/audit-request/?source=revenue_leak_evidence_packet",
        "revenue leak evidence packet tracked request route",
    ),
    RequiredLink(
        "/nextjs-supabase-stripe-setup-help/",
        "/go/billing-reliability/setup-request/?source=setup_help_cta",
        "setup help tracked request route",
    ),
    RequiredLink(
        "/nextjs-supabase-stripe-setup-help/",
        "/go/billing-reliability/setup-request/?source=live_money_gate",
        "live-money tracked request route",
    ),
    RequiredLink(
        "/billing-health-support/",
        "/go/billing-reliability/health-support/?source=billing_health_cta",
        "billing-health tracked request route",
    ),
    RequiredLink(
        "/go/billing-reliability/audit-request/",
        "revenue_leak_audit_request_mailto_opened",
        "audit route mailto-open event",
    ),
    RequiredLink(
        "/go/billing-reliability/setup-request/",
        "setup_help_request_mailto_opened",
        "setup route mailto-open event",
    ),
    RequiredLink(
        "/go/billing-reliability/health-support/",
        "billing_health_request_mailto_opened",
        "billing-health route mailto-open event",
    ),
    RequiredLink(
        "/blog/stripe-invoice-paid-double-extends-supabase-membership/",
        "/blog/stripe-subscription-monthly-credits-double-grant-supabase/?ref=invoice_paid_monthly_credit_context",
        "invoice paid monthly credit contextual link",
    ),
    RequiredLink(
        "/blog/stripe-invoice-paid-double-extends-supabase-membership/",
        "/blog/stripe-subscription-monthly-credits-double-grant-supabase/?ref=invoice_paid_monthly_credit_bottom",
        "invoice paid monthly credit bottom CTA",
    ),
    RequiredLink(
        "/blog/stripe-webhook-event-ordering-supabase/",
        "/blog/stripe-subscription-monthly-credits-double-grant-supabase/?ref=event_ordering_monthly_credit_context",
        "event ordering monthly credit contextual link",
    ),
    RequiredLink(
        "/blog/stripe-webhook-event-ordering-supabase/",
        "/blog/stripe-subscription-monthly-credits-double-grant-supabase/?ref=event_ordering_monthly_credit_related",
        "event ordering monthly credit related link",
    ),
    RequiredLink(
        "/blog/stripe-charged-customer-not-provisioned-supabase/",
        "/blog/stripe-hosted-plan-entitlement-provisioning-supabase/?ref=charged_stranded_hosted_plan_context",
        "charged stranded hosted-plan contextual link",
    ),
    RequiredLink(
        "/blog/stripe-charged-customer-not-provisioned-supabase/",
        "/blog/stripe-hosted-plan-entitlement-provisioning-supabase/?ref=charged_stranded_bottom_hosted_plan",
        "charged stranded hosted-plan bottom CTA",
    ),
    RequiredLink(
        "/blog/stripe-checkout-success-url-webhook-access/",
        "/blog/stripe-hosted-plan-entitlement-provisioning-supabase/?ref=checkout_success_hosted_plan_context",
        "checkout success hosted-plan contextual link",
    ),
    RequiredLink(
        "/blog/stripe-checkout-success-url-webhook-access/",
        "/blog/stripe-hosted-plan-entitlement-provisioning-supabase/?ref=checkout_success_bottom_hosted_plan",
        "checkout success hosted-plan bottom CTA",
    ),
    RequiredLink(
        "/blog/stripe-hosted-plan-entitlement-provisioning-supabase/",
        "billing_reliability_section_reached",
        "hosted-plan evidence packet section view event",
    ),
    RequiredLink(
        "/blog/stripe-hosted-plan-entitlement-provisioning-supabase/",
        "hosted_plan_entitlement_evidence_packet",
        "hosted-plan evidence packet section location",
    ),
    RequiredLink(
        "/blog/stripe-subscription-add-credit-checkout-ledger/",
        "billing_reliability_section_reached",
        "subscription add-credit evidence packet section view event",
    ),
    RequiredLink(
        "/blog/stripe-subscription-add-credit-checkout-ledger/",
        "subscription_add_credit_evidence_packet",
        "subscription add-credit evidence packet section location",
    ),
]


class CTAParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ctas: list[dict[str, str]] = []
        self.scripts: list[str] = []
        self._in_script = False
        self._script_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        if "data-ph-event" in attr_map:
            self.ctas.append(attr_map)
        if tag.lower() == "script":
            self._in_script = True
            self._script_chunks = []

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self._script_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_script:
            self.scripts.append("".join(self._script_chunks))
            self._in_script = False
            self._script_chunks = []


def page_file(route: str) -> Path:
    return SITE_ROOT / route.strip("/") / "index.html"


def parse_page(route: str) -> tuple[list[dict[str, str]], str]:
    file_path = page_file(route)
    html = file_path.read_text(encoding="utf-8")
    parser = CTAParser()
    parser.feed(html)
    return parser.ctas, "\n".join(parser.scripts)


def page_html(route: str) -> str:
    return page_file(route).read_text(encoding="utf-8")


def location_matches(cta: dict[str, str], requirement: RequiredEvent) -> bool:
    if cta.get("data-ph-event") != requirement.event:
        return False
    if requirement.location and cta.get("data-ph-location") != requirement.location:
        return False
    if requirement.product and (cta.get("data-ph-product") or "") not in ("", requirement.product):
        return False
    return True


def has_dynamic_score_attrs(ctas: list[dict[str, str]], script_text: str, requirement: RequiredEvent) -> bool:
    matching = [cta for cta in ctas if location_matches(cta, requirement)]
    if not matching:
        return False
    for attr in ("data-ph-score", "data-ph-risk-count", "data-ph-recommended-scope"):
        if any(cta.get(attr) for cta in matching):
            continue
        if re.search(rf"setAttribute\(['\"]{re.escape(attr)}['\"]", script_text):
            continue
        return False
    return True


def has_required_product(cta: dict[str, str], requirement: RequiredEvent) -> bool:
    if not requirement.product:
        return True
    if not requirement.require_product and not cta.get("href", "").startswith("mailto:"):
        return True
    return cta.get("data-ph-product") == requirement.product


def audit() -> tuple[list[str], list[str]]:
    failures: list[str] = []
    lines: list[str] = []
    grouped: dict[str, list[RequiredEvent]] = {}
    for requirement in REQUIRED_EVENTS:
        grouped.setdefault(requirement.path, []).append(requirement)

    for route, requirements in grouped.items():
        file_path = page_file(route)
        if not file_path.exists():
            failures.append(f"{route}: missing {file_path}")
            continue
        ctas, script_text = parse_page(route)
        lines.append(f"## {route}")
        lines.append(f"- CTA count: {len(ctas)}")
        for requirement in requirements:
            matches = [cta for cta in ctas if location_matches(cta, requirement)]
            if not matches:
                failures.append(f"{route}: missing {requirement.event} at {requirement.location}")
                lines.append(f"- FAIL `{requirement.event}` / `{requirement.location}`")
                continue
            missing_product = [cta for cta in matches if not has_required_product(cta, requirement)]
            if missing_product:
                failures.append(f"{route}: missing data-ph-product={requirement.product} for {requirement.event} at {requirement.location}")
                lines.append(f"- FAIL `{requirement.event}` / `{requirement.location}` product")
                continue
            if requirement.needs_score_attrs and not has_dynamic_score_attrs(ctas, script_text, requirement):
                failures.append(f"{route}: missing score/risk/scope attrs for {requirement.event} at {requirement.location}")
                lines.append(f"- FAIL `{requirement.event}` / `{requirement.location}` score attrs")
                continue
            hrefs = ", ".join(sorted({cta.get("href", "") for cta in matches if cta.get("href")}))
            lines.append(f"- OK `{requirement.event}` / `{requirement.location}`" + (f" -> {hrefs}" if hrefs else ""))
        lines.append("")
    link_grouped: dict[str, list[RequiredLink]] = {}
    for requirement in REQUIRED_LINKS:
        link_grouped.setdefault(requirement.path, []).append(requirement)

    for route, requirements in link_grouped.items():
        file_path = page_file(route)
        if not file_path.exists():
            failures.append(f"{route}: missing {file_path}")
            continue
        html = page_html(route)
        lines.append(f"## {route} links")
        for requirement in requirements:
            if requirement.href not in html:
                failures.append(f"{route}: missing link {requirement.label} -> {requirement.href}")
                lines.append(f"- FAIL `{requirement.label}` -> {requirement.href}")
                continue
            lines.append(f"- OK `{requirement.label}` -> {requirement.href}")
        lines.append("")
    return failures, lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true", help="print a markdown audit report")
    args = parser.parse_args()

    failures, lines = audit()
    if args.markdown:
        print("# Billing reliability event coverage audit\n")
        print("Static local check. This does not query PostHog or prove real traffic.\n")
        print("\n".join(lines))
    if failures:
        print("BILLING_RELIABILITY_EVENT_AUDIT_FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("BILLING_RELIABILITY_EVENT_AUDIT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
