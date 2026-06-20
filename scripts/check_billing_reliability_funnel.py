#!/usr/bin/env python3
import sys
import time
import urllib.request

HOST = "https://goosekit.dev"

PAGES = [
    {
        "path": "/stripe-supabase-billing-drift-check/",
        "required": [
            "billing_drift_review_request",
            "revenue_leak_audit_interest",
            "setup_help_retainer_interest",
            "Debug packet for a paid review",
            "Stripe object ids",
            "Stripe object ids you can share",
            "Supabase rows or table names involved",
            "What the paid user currently sees",
            "Webhook delivery status or error",
            "One state that must be true after review",
            "First paid review scope",
            "€99 narrow review",
            "€149 revenue leak audit",
            "Not a broad rebuild",
            "id=\"monthlyCta\"",
            "client-supplied plan, paid, or isPro flags",
            "Hosted-plan, tenant, or workspace provisioning can be replayed from Stripe truth without duplicate access",
            "Entitlement or access row before/after replay",
            "Tenant/workspace provisioning job or result",
            "Monthly credit, usage, or quota refills use one cycle key",
            "One-time add-credit purchases and monthly subscription credits write through one replay-safe credit ledger",
            "Stripe Connect transfer reversals update payout balance, commission state, and clawback queue exactly once under duplicate delivery",
            "For Stripe Connect: transfer id, payout balance row, commission row, clawback queue row, and the replay/idempotency result",
            "data-risk-key=\"subscription_add_credit\"",
            "data-risk-key=\"missing_subscription_columns\"",
            "data-ph-unchecked-risk-keys",
            "schema drift between subscriptions and plan config",
            "Subscriptions table schema:",
            "Pricing_config or plan-limit schema:",
            "Attempted webhook/check-subscription columns:",
            "Billing trouble events raise and resolve durable action queue or retention cards",
            "Monthly credit/refill row or tier cap config",
            "One-time add-credit Checkout event or payment object",
            "Credit ledger or balance row after subscription and add-credit",
            "Grant function or webhook log for both credit paths",
            "Action queue or retention card row",
            "Billing ledger or processed-event row",
            "23505 retry storms",
            "Known duplicate event IDs return 2xx after a 23505 conflict",
            "23505 duplicate-key log or processed-event conflict",
            "HTTP response Stripe saw after duplicate delivery",
            "data-ph-product=\"billing_reliability\"",
            "data-ph-recommended-scope=\"unscored\"",
            "setup_help_secondary_clicked",
            "billing_drift_check_secondary",
        ],
    },
    {
        "path": "/stripe-billing-reliability-checklist/",
        "required": [
            "billing_drift_check_clicked",
            "setup_help_request_clicked",
            "revenue_leak_audit_interest",
            "data-ph-product=\"billing_reliability\"",
            "data-ph-event=\"billing_drift_check_clicked\" data-ph-product=\"billing_reliability\" data-ph-location=\"billing_reliability_checklist_top\"",
            "data-ph-event=\"setup_help_retainer_interest\" data-ph-product=\"billing_reliability\" data-ph-location=\"billing_reliability_checklist_top\"",
            "data-ph-event=\"billing_drift_check_clicked\" data-ph-product=\"billing_reliability\" data-ph-location=\"billing_reliability_checklist_bottom\"",
            "data-ph-event=\"setup_help_retainer_interest\" data-ph-product=\"billing_reliability\" data-ph-location=\"billing_reliability_checklist_bottom\"",
            "Evidence packet for a paid review",
            "billing_reliability_evidence_packet",
            "data-ph-event=\"billing_reliability_evidence_packet\" data-ph-product=\"billing_reliability\" data-ph-location=\"billing_reliability_evidence_packet\"",
            "expected app state",
            "actual app state",
            "user-visible symptom",
            "data-ph-event=\"setup_help_secondary_clicked\" data-ph-product=\"billing_reliability\" data-ph-location=\"billing_reliability_checklist_bottom\"",
        ],
    },
    {
        "path": "/stripe-supabase-revenue-leak-audit/",
        "required": [
            "revenue_leak_audit_request_clicked",
            "billing_drift_check_clicked",
            "setup_help_retainer_interest",
            "data-ph-product=\"billing_reliability\"",
            "€149",
            "fixed founding pass",
            "Paid but blocked",
            "Unpaid but unlocked",
            "Provider truth",
            "App truth",
            "Audit output",
            "Send a small evidence packet first",
            "revenue_leak_evidence_packet",
            "/go/billing-reliability/audit-request/?source=revenue_leak_audit_cta",
            "/go/billing-reliability/audit-request/?source=revenue_leak_evidence_packet",
            "Expected app state and actual app state",
            "data-ph-event=\"setup_help_secondary_clicked\" data-ph-product=\"billing_reliability\" data-ph-location=\"revenue_leak_audit_bottom\"",
            "data-ph-event=\"setup_help_retainer_interest\" data-ph-product=\"billing_reliability\" data-ph-location=\"revenue_leak_audit_bottom\"",
        ],
    },
    {
        "path": "/billing-health-support/",
        "required": [
            "billing_health_interest",
            "revenue_leak_audit_interest",
            "data-ph-product=\"billing_reliability\"",
            "What this is not",
            "billing_health_live_money_gate",
            "billing-action-queue-review",
            "billing_action_queue_review",
            "Action queues",
            "Billing action queue review",
            "billing_action_queue_packet_mailto",
            "Send action-queue evidence",
            "Use the checklist first",
            "Founding-5 intake filter",
            "Stripe event, invoice, subscription, customer, or Checkout Session id",
            "Supabase table or row that controls paid access",
            "billing action queue",
            "/go/billing-reliability/health-support/?source=billing_health_cta",
        ],
    },
    {
        "path": "/ship-it-kit-setup-help/",
        "required": [
            "billing_health_interest",
            "data-ph-product=\"billing_reliability\"",
            "shipit_setup_help_hero_retainer",
            "founding-5 €29/mo billing-health support",
            "Where monthly support fits",
        ],
    },
    {
        "path": "/nextjs-supabase-stripe-setup-help/",
        "required": [
            "setup_help_request_clicked",
            "live_money_gate_block",
            "revenue_leak_audit_interest",
            "data-ph-product=\"billing_reliability\"",
            "/go/billing-reliability/setup-request/?source=setup_help_cta",
            "/go/billing-reliability/setup-request/?source=live_money_gate",
            "data-ph-event=\"setup_help_retainer_interest\" data-ph-product=\"billing_reliability\" data-ph-location=\"retainer_block\"",
            "data-ph-event=\"setup_help_retainer_interest\" data-ph-product=\"billing_reliability\" data-ph-location=\"setup_help_artifacts_monthly_support\"",
        ],
    },
    {
        "path": "/go/billing-reliability/audit-request/?v=audit_route_context",
        "required": [
            "noindex, nofollow",
            "Stripe + Supabase audit",
            "revenue_leak_audit_request_route_viewed",
            "revenue_leak_audit_request_manual_click",
            "revenue_leak_audit_request_mailto_opened",
            "source_ref: source",
            "request_context: 'revenue_leak_audit'",
            "price_range_eur: '149'",
            "target_href: mailto",
            "price_eur: 149",
            "Source%3A%20",
        ],
    },
    {
        "path": "/go/billing-reliability/setup-request/?v=setup_route_context",
        "required": [
            "noindex, nofollow",
            "Next.js + Supabase + Stripe",
            "setup_help_request_route_viewed",
            "setup_help_request_manual_click",
            "setup_help_request_mailto_opened",
            "setup_help_request_copy_clicked",
            "setup_help_request_email_copy_clicked",
            "setup_help_request_subject_copy_clicked",
            "setup_help_request_gmail_clicked",
            "setup_help_request_outlook_clicked",
            "setup_help_request_form_started",
            "setup_help_request_field_completed",
            "setup_help_request_ready_to_send",
            "setup_help_request_formspree_submit",
            "/go/billing-reliability/setup-request-sent/",
            "setup_help_request_auto_mailto_suppressed",
            "https://formspree.io/f/xblgwdqz",
            "name=\"_next\"",
            "name=\"request_packet\"",
            "data-button-position=\"after_form\"",
            "data-request-field=\"blocker\"",
            "location: 'setup_help_request_route'",
            "path: '/go/billing-reliability/setup-request/'",
            "target_href: window.location.href",
            "target_href: links.mailto",
            "request_context: context",
            "price_range_eur: priceRange",
            "ship_it_kit_setup_help",
            "199-plus",
            "Source: ",
        ],
    },
    {
        "path": "/go/billing-reliability/setup-request-sent/?v=setup_route_sent",
        "required": [
            "noindex, nofollow",
            "Request sent",
            "setup_help_request_formspree_returned",
            "setup_help_request_sent_route",
            "price_range_eur",
            "/ship-it-kit-setup-help/",
        ],
    },
    {
        "path": "/go/billing-reliability/health-support/?v=health_route_context",
        "required": [
            "noindex, nofollow",
            "Billing-health support",
            "billing_health_request_route_viewed",
            "billing_health_request_manual_click",
            "billing_health_request_mailto_opened",
            "billing_health_request_form_started",
            "billing_health_request_field_completed",
            "billing_health_request_ready_to_send",
            "billing_health_request_formspree_submit",
            "billing_health_request_copy_clicked",
            "https://formspree.io/f/xblgwdqz",
            "name=\"request_packet\"",
            "name=\"_next\"",
            "/go/billing-reliability/health-support-sent/",
            "source_ref: source",
            "request_context: 'billing_health_support'",
            "price_range_eur: '29/mo'",
            "target_href: mailto",
            "price_eur_monthly: 29",
            "Monthly billing risk",
            "Evidence ready",
        ],
    },
    {
        "path": "/go/billing-reliability/health-support-sent/?v=health_route_sent",
        "required": [
            "noindex, nofollow",
            "Request sent",
            "billing_health_request_formspree_returned",
            "billing_health_request_sent_route",
            "price_eur_monthly: 29",
        ],
    },
    {
        "path": "/blog/stripe-webhook-supabase-paid-status/",
        "required": [
            "billing_drift_check_clicked",
            "webhook_paid_status_top",
            "paid access starts jobs",
            "terminal Stripe status",
            "monthly run cap",
            "credit reservation",
            "repairable reservation row",
        ],
    },
    {
        "path": "/blog/stripe-webhook-duplicate-events-idempotency-supabase/",
        "required": [
            "billing_drift_check_clicked",
            "duplicate_webhook_top",
            "duplicate_webhook_23505_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "23505",
            "retry storm",
            "Processed-event or stripe_events row before/after",
            "HTTP response Stripe saw",
        ],
    },
    {
        "path": "/blog/stripe-webhook-event-ordering-supabase/",
        "required": [
            "billing_drift_check_clicked",
            "event_ordering_top",
            "event_ordering_monthly_credit_context",
            "event_ordering_monthly_credit_related",
        ],
    },
    {
        "path": "/blog/stripe-trial-ending-supabase-access/",
        "required": ["billing_drift_check_clicked", "trial_top"],
    },
    {
        "path": "/blog/stripe-dunning-past-due-unpaid-supabase-access/",
        "required": ["billing_drift_check_clicked", "dunning_top"],
    },
    {
        "path": "/blog/stripe-customer-portal-cancel-supabase-status/",
        "required": ["billing_drift_check_clicked", "portal_cancel_top"],
    },
    {
        "path": "/blog/stripe-customer-portal-plan-change-supabase-entitlements/",
        "required": ["billing_drift_check_clicked", "portal_plan_change_top"],
    },
    {
        "path": "/blog/stripe-charged-customer-not-provisioned-supabase/",
        "required": ["billing_drift_check_clicked", "charged_stranded_top"],
    },
    {
        "path": "/blog/stripe-duplicate-subscription-supabase-access/",
        "required": ["billing_drift_check_clicked", "duplicate_subscription_top"],
    },
    {
        "path": "/blog/stripe-invoice-paid-double-extends-supabase-membership/",
        "required": [
            "billing_drift_check_clicked",
            "invoice_paid_double_extend_top",
            "invoice_paid_double_extend_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "invoice_paid_monthly_credit_context",
            "invoice_paid_monthly_credit_bottom",
        ],
    },
    {
        "path": "/blog/stripe-client-paid-flag-supabase-bypass/",
        "required": [
            "billing_drift_check_clicked",
            "paid_flag_bypass_top",
            "paid_flag_bypass_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "failed entitlement write",
            "retryable processed-event or repair record",
            "checkout success page cannot write a Pro profile value",
        ],
    },
    {
        "path": "/blog/saas-credits-deducted-job-failed-no-refund/",
        "required": [
            "billing_drift_check_clicked",
            "metered_credit_job_failed_top",
            "metered_credit_job_failed_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "terminal state",
            "debit helper",
            "job/output row",
            "refund or repair record",
            "no-op edits",
            "input asset hash",
            "no-op detection rule",
        ],
    },
    {
        "path": "/blog/stripe-checkout-success-url-webhook-access/",
        "required": [
            "billing_drift_check_clicked",
            "checkout_success_webhook_top",
            "checkout_success_webhook_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "success URL",
            "webhook-owned subscription truth",
            "duplicate checkout.session.completed",
            "local subscription row",
            "checkout_success_hosted_plan_context",
            "checkout_success_bottom_hosted_plan",
        ],
    },
    {
        "path": "/blog/stripe-setup-mode-card-on-file-subscription-gate/",
        "required": [
            "billing_drift_check_clicked",
            "setup_mode_card_gate_top",
            "setup_mode_card_gate_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "mode: setup",
            "SetupIntent metadata",
            "job/backfill gate",
            "payment method state",
        ],
    },
    {
        "path": "/blog/stripe-subscription-monthly-credits-double-grant-supabase/",
        "required": [
            "billing_drift_check_clicked",
            "monthly_credit_grant_top",
            "monthly_credit_refill_packet_mailto",
            "monthly_credit_refill_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "invoice.paid",
            "RevenueCat",
            "usage_balances",
            "tier cap",
            "fallback cron",
            "non-additive",
        ],
    },
    {
        "path": "/blog/stripe-subscription-add-credit-checkout-ledger/",
        "required": [
            "billing_drift_check_clicked",
            "subscription_add_credit_top",
            "subscription_add_credit_packet_mailto",
            "subscription_add_credit_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "checkout.session.completed",
            "invoice.paid",
            "credit ledger",
            "monthly reset",
            "one-time add-credit",
        ],
    },
    {
        "path": "/blog/stripe-one-time-booking-subscription-credit-atomic/",
        "required": [
            "billing_drift_check_clicked",
            "one_time_booking_top",
            "one_time_booking_bottom_mailto",
            "setup_help_retainer_interest",
            "data-ph-product=\"billing_reliability\"",
            "fail-before-charge",
            "Booking/session row before/after",
            "Subscription credit row before/after",
            "Processed-event or idempotency row",
            "Refund, release, or repair path",
        ],
    },
    {
        "path": "/blog/stripe-webhook-supabase-missing-subscription-columns/",
        "required": [
            "billing_drift_check_clicked",
            "missing_subscription_columns_top",
            "missing_subscription_columns_bottom_mailto",
            "setup_help_retainer_interest",
            "data-ph-product=\"billing_reliability\"",
            "subscriptions table schema",
            "Pricing_config or plan-limit table schema",
            "Webhook write attempted columns",
            "check-subscription write attempted columns",
            "Processed-event/idempotency row",
        ],
    },
    {
        "path": "/blog/stripe-payment-element-redirect-webhook-order-tracking/",
        "required": [
            "billing_drift_check_clicked",
            "payment_element_order_tracking_top",
            "payment_element_order_tracking_bottom_mailto",
            "setup_help_retainer_interest",
            "data-ph-product=\"billing_reliability\"",
            "PaymentIntent or Checkout Session id",
            "return_url and redirect_status received",
            "Webhook event id, type, delivery status",
            "Order row before/after webhook",
            "Realtime payload or subscription log",
            "Expected order/tracking state",
            "Actual order/tracking bug",
        ],
    },
    {
        "path": "/blog/stripe-charged-customer-not-provisioned-supabase/",
        "required": [
            "billing_drift_check_clicked",
            "charged_stranded_top",
            "charged_stranded_hosted_plan_context",
            "charged_stranded_bottom_hosted_plan",
        ],
    },
    {
        "path": "/blog/stripe-hosted-plan-entitlement-provisioning-supabase/",
        "required": [
            "billing_drift_check_clicked",
            "hosted_plan_entitlement_top",
            "hosted_plan_entitlement_packet_mailto",
            "hosted_plan_entitlement_bottom_mailto",
            "data-ph-product=\"billing_reliability\"",
            "entitlement resolver",
            "tenant provisioning",
            "billing event ledger",
            "provisioning job/result",
            "billing_reliability_section_reached",
            "hosted_plan_entitlement_evidence_packet",
        ],
    },
    {
        "path": "/blog/stripe-connect-transfer-reversed-clawback-ledger/",
        "required": [
            "billing_drift_check_clicked",
            "connect_transfer_reversal_top",
            "revenue_leak_audit_interest",
            "setup_help_request_clicked",
            "connect_transfer_reversal_bottom_mailto",
            "setup_help_secondary_clicked",
            "connect_transfer_reversal_related",
            "data-ph-product=\"billing_reliability\"",
            "transfer.reversed",
            "payout balance",
            "commission",
            "clawback queue",
            "Replay command, test, or local repro",
        ],
    },
    {
        "path": "/blog/stripe-connect-affiliate-revenue-share-ledger/",
        "required": [
            "billing_drift_check_clicked",
            "affiliate_revenue_share_top",
            "revenue_leak_audit_interest",
            "setup_help_request_clicked",
            "affiliate_revenue_share_bottom_mailto",
            "setup_help_secondary_clicked",
            "affiliate_revenue_share_related",
            "data-ph-product=\"billing_reliability\"",
            "creator earnings ledger",
            "affiliate attribution",
            "self-referral",
            "refund reversal",
            "payout batch",
            "Replay command, test, or local repro",
        ],
    },
    {
        "path": "/blog/stripe-course-membership-supabase-access/",
        "required": [
            "billing_drift_check_clicked",
            "course_membership_top",
            "course_membership_bottom_mailto",
            "setup_help_retainer_interest",
            "data-ph-product=\"billing_reliability\"",
            "course membership",
            "has_active_subscription()",
            "is_entitled(course_id)",
            "Per-course grant or access-code row",
            "Stripe price env vars involved",
        ],
    },
    {
        "path": "/blog/stripe-zalopay-revenuecat-supabase-subscriptions/",
        "required": [
            "billing_drift_check_clicked",
            "multi_provider_subscription_top",
            "multi_provider_subscription_bottom_mailto",
            "setup_help_retainer_interest",
            "data-ph-product=\"billing_reliability\"",
            "Stripe",
            "ZaloPay",
            "RevenueCat",
            "Supabase subscriptions row before/after",
            "Provider event ids and statuses",
            "Processed-event or idempotency row",
            "Duplicate/replay result",
        ],
    },
    {
        "path": "/blog/stripe-prepaid-invoice-account-credit-ledger/",
        "required": [
            "billing_drift_check_clicked",
            "prepaid_credit_top",
            "prepaid_credit_bottom_mailto",
            "setup_help_retainer_interest",
            "data-ph-product=\"billing_reliability\"",
            "customer_credit_ledger",
            "customers.account_credits",
            "credit_applied",
            "prepaid_at",
            "Expected revenue-recognition state",
        ],
    },
]


def fetch(path: str) -> tuple[int, str]:
    separator = "&" if "?" in path else "?"
    req = urllib.request.Request(
        f"{HOST}{path}{separator}funnel_check=1&ts={int(time.time())}",
        headers={"User-Agent": "goosekit-billing-funnel-check/1.0", "Cache-Control": "no-cache"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        body = response.read().decode("utf-8", errors="replace")
        return response.status, body


def main() -> int:
    failures: list[str] = []
    for page in PAGES:
        path = page["path"]
        try:
            status, body = fetch(path)
        except Exception as exc:
            failures.append(f"{path}: fetch failed: {exc}")
            continue

        if status != 200:
            failures.append(f"{path}: expected HTTP 200, got {status}")
            continue

        missing = [needle for needle in page["required"] if needle not in body]
        if missing:
            failures.append(f"{path}: missing {', '.join(missing)}")
            continue

        print(f"OK {path}")

    if failures:
        print("BILLING_RELIABILITY_FUNNEL_FAIL", file=sys.stderr)
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("BILLING_RELIABILITY_FUNNEL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
