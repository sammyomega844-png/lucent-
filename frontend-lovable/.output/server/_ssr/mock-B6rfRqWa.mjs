//#region node_modules/.nitro/vite/services/ssr/assets/mock-B6rfRqWa.js
var action_register_default = {
	generated_at: "2026-07-01T04:03:52.948773+00:00",
	counts: {
		"total": 2,
		"tasks": 2,
		"emails": 0,
		"slack": 0,
		"reply_drafts": 0
	},
	summary: "Unified action register: 2 item(s) total; 0 reply draft(s), 2 task(s), 0 email(s), 0 Slack item(s).",
	items: [{
		"source": "task",
		"title": "Database Setup",
		"owner": "Charlie",
		"due_date": "2024-01-20",
		"priority": "High",
		"score": 90,
		"reason": "high priority, due 2024-01-20, in progress"
	}, {
		"source": "task",
		"title": "UI Wireframes",
		"owner": "Bob",
		"due_date": "2024-01-15",
		"priority": "Medium",
		"score": 75,
		"reason": "due 2024-01-15, in progress"
	}]
};
var follow_up_plan_default = {
	generated_at: "2026-07-01T04:03:52.989129+00:00",
	counts: {
		"total": 4,
		"tasks": 4,
		"reply_drafts": 0,
		"email_slack": 0
	},
	summary: "Follow-up autopilot: 4 item(s) ready; 0 approval draft(s), 4 overdue task(s), 0 inbox/chat follow-up(s).",
	items: [
		{
			"source": "task",
			"title": "UI Wireframes",
			"owner": "Bob",
			"due_date": "2024-01-15",
			"priority": "Medium",
			"score": 80,
			"reason": "overdue by 898 day(s)",
			"nudge_subject": "Follow up: UI Wireframes",
			"nudge_body": "Hi Bob, just following up on UI Wireframes. It was due on 2024-01-15 and is now 898 day(s) overdue. Please send a quick status update or confirm the new deadline."
		},
		{
			"source": "task",
			"title": "Database Setup",
			"owner": "Charlie",
			"due_date": "2024-01-20",
			"priority": "High",
			"score": 80,
			"reason": "overdue by 893 day(s)",
			"nudge_subject": "Follow up: Database Setup",
			"nudge_body": "Hi Charlie, just following up on Database Setup. It was due on 2024-01-20 and is now 893 day(s) overdue. Please send a quick status update or confirm the new deadline."
		},
		{
			"source": "task_followup",
			"title": "Database Setup",
			"owner": "Charlie",
			"due_date": "2024-01-20",
			"priority": "High",
			"score": 70,
			"reason": "high priority, due 2024-01-20, in progress",
			"nudge_subject": "Follow up: Database Setup",
			"nudge_body": "Hi Charlie, checking in on Database Setup. It is still active in the action register because it needs attention. Please share a status update or next step."
		},
		{
			"source": "task_followup",
			"title": "UI Wireframes",
			"owner": "Bob",
			"due_date": "2024-01-15",
			"priority": "Medium",
			"score": 70,
			"reason": "due 2024-01-15, in progress",
			"nudge_subject": "Follow up: UI Wireframes",
			"nudge_body": "Hi Bob, checking in on UI Wireframes. It is still active in the action register because it needs attention. Please share a status update or next step."
		}
	]
};
var meeting_execution_plan_default = {
	generated_at: "2026-07-01T04:03:53.015309+00:00",
	counts: {
		"total": 2,
		"meeting_notes": 0,
		"action_register": 2,
		"follow_up": 0
	},
	summary: "Meeting-to-execution: 2 item(s) ready; 0 from notes, 2 from the action register, 0 from follow-up autopilot.",
	items: [{
		"source": "task_meeting",
		"title": "UI Wireframes",
		"owner": "Bob",
		"due_date": "2024-01-15",
		"priority": "Medium",
		"score": 90,
		"reason": "overdue by 898 day(s)",
		"next_step": "Turn this into a concrete action with an owner and deadline."
	}, {
		"source": "task_meeting",
		"title": "Database Setup",
		"owner": "Charlie",
		"due_date": "2024-01-20",
		"priority": "High",
		"score": 90,
		"reason": "overdue by 893 day(s)",
		"next_step": "Turn this into a concrete action with an owner and deadline."
	}]
};
var customer_health_report_default = {
	generated_at: "2026-07-01T04:03:53.071811+00:00",
	summary: "Customer health radar: 3 lead(s) scored; 1 healthy; 1 watch; 1 at risk; top risk Ross Law (23/100); top opportunity TechInc (82/100).",
	counts: {
		"total": 3,
		"healthy": 1,
		"watch": 1,
		"risk": 1
	},
	items: [
		{
			"source": "crm",
			"company": "TechInc",
			"lead_name": "John Doe",
			"status": "Qualified",
			"lead_value": 5e3,
			"score": 82,
			"bucket": "healthy",
			"reason": "Qualified, contacted 905 day(s) ago, 0 related open item(s)",
			"next_step": "Keep cadence and expand the account.",
			"related_open_items": 0
		},
		{
			"source": "crm",
			"company": "WebSoft",
			"lead_name": "Sara Smith",
			"status": "Contacted",
			"lead_value": 2500,
			"score": 68,
			"bucket": "watch",
			"reason": "Contacted, contacted 906 day(s) ago, 0 related open item(s)",
			"next_step": "Send a follow-up and confirm next milestone.",
			"related_open_items": 0
		},
		{
			"source": "crm",
			"company": "Ross Law",
			"lead_name": "Mike Ross",
			"status": "Lost",
			"lead_value": 0,
			"score": 23,
			"bucket": "risk",
			"reason": "Lost, contacted 903 day(s) ago, 0 related open item(s)",
			"next_step": "Escalate and re-engage before the lead stalls.",
			"related_open_items": 0
		}
	]
};
var pipeline_risk_report_default = {
	generated_at: "2026-07-01T04:03:53.140838+00:00",
	summary: "Pipeline risk radar: 2 active deal(s) scored; 2 at risk; 0 watch; 0 stable; top risk TechInc (99/100); highest value TechInc ($5,000).",
	counts: {
		"total": 2,
		"risk": 2,
		"watch": 0,
		"stable": 0,
		"closed_lost": 1
	},
	items: [{
		"source": "crm",
		"company": "TechInc",
		"lead_name": "John Doe",
		"status": "Qualified",
		"lead_value": 5e3,
		"score": 99,
		"bucket": "risk",
		"reason": "Qualified, touched 905 day(s) ago, 0 related open item(s)",
		"next_step": "Escalate now and reset the close plan.",
		"related_open_items": 0
	}, {
		"source": "crm",
		"company": "WebSoft",
		"lead_name": "Sara Smith",
		"status": "Contacted",
		"lead_value": 2500,
		"score": 87,
		"bucket": "risk",
		"reason": "Contacted, touched 906 day(s) ago, 0 related open item(s)",
		"next_step": "Escalate now and reset the close plan.",
		"related_open_items": 0
	}]
};
var approval_workflow_default = {
	generated_at: "2026-07-01T04:03:53.243872+00:00",
	summary: "Approval workflow: no pending drafts.",
	counts: {
		"total_pending": 0,
		"total_approved": 0,
		"total_rejected": 0,
		"total_sent": 0,
		"showing": 0
	},
	items: []
};
var kpi_digest_report_default = {
	generated_at: "2026-07-01T04:03:53.365560+00:00",
	summary: "KPI digest: 5 day(s) of data; 2 KPI(s) declining — review flags; pipeline $7,500, 1 qualified, 0 overdue task(s).",
	kpis: {
		"completed_tasks": {
			"latest": 1,
			"avg": 1,
			"trend": "stable"
		},
		"high_priority_open": {
			"latest": 1,
			"avg": .8,
			"trend": "declining"
		},
		"overdue_tasks": {
			"latest": 0,
			"avg": 0,
			"trend": "stable"
		},
		"stock_alerts": {
			"latest": 1,
			"avg": .8,
			"trend": "declining"
		},
		"qualified_leads": {
			"latest": 1,
			"avg": 1,
			"trend": "stable"
		},
		"pipeline_value": {
			"latest": 7500,
			"avg": 7500,
			"trend": "stable"
		},
		"lost_deals": {
			"latest": 1,
			"avg": 1,
			"trend": "stable"
		}
	},
	rows: [
		{
			"completed_tasks": 1,
			"high_priority_open": 0,
			"overdue_tasks": 0,
			"stock_alerts": 0,
			"qualified_leads": 1,
			"pipeline_value": 7500,
			"lost_deals": 1,
			"date": "2026-06-17"
		},
		{
			"completed_tasks": 1,
			"high_priority_open": 1,
			"overdue_tasks": 0,
			"stock_alerts": 1,
			"qualified_leads": 1,
			"pipeline_value": 7500,
			"lost_deals": 1,
			"date": "2026-06-22"
		},
		{
			"completed_tasks": 1,
			"high_priority_open": 1,
			"overdue_tasks": 0,
			"stock_alerts": 1,
			"qualified_leads": 1,
			"pipeline_value": 7500,
			"lost_deals": 1,
			"date": "2026-06-23"
		},
		{
			"completed_tasks": 1,
			"high_priority_open": 1,
			"overdue_tasks": 0,
			"stock_alerts": 1,
			"qualified_leads": 1,
			"pipeline_value": 7500,
			"lost_deals": 1,
			"date": "2026-06-26"
		},
		{
			"completed_tasks": 1,
			"high_priority_open": 1,
			"overdue_tasks": 0,
			"stock_alerts": 1,
			"qualified_leads": 1,
			"pipeline_value": 7500,
			"lost_deals": 1,
			"date": "2026-06-30"
		}
	],
	flags: ["high priority open is declining (latest 1, avg 0.8)", "stock alerts is declining (latest 1, avg 0.8)"]
};
var communication_timeline_default = {
	generated_at: "2026-07-01T04:03:53.399501+00:00",
	summary: "Communication timeline: 3 account(s); 2 active; 3 total touches recorded.",
	accounts: {
		"TechInc": {
			"lead_name": "John Doe",
			"status": "Qualified",
			"lead_value": 5e3,
			"last_contact": "2024-01-08",
			"touch_count": 1,
			"touches": [{
				"source": "crm",
				"date": "2024-01-08",
				"summary": "CRM record — status: Qualified, value: $5000",
				"type": "crm"
			}]
		},
		"WebSoft": {
			"lead_name": "Sara Smith",
			"status": "Contacted",
			"lead_value": 2500,
			"last_contact": "2024-01-07",
			"touch_count": 1,
			"touches": [{
				"source": "crm",
				"date": "2024-01-07",
				"summary": "CRM record — status: Contacted, value: $2500",
				"type": "crm"
			}]
		},
		"Ross Law": {
			"lead_name": "Mike Ross",
			"status": "Lost",
			"lead_value": 0,
			"last_contact": "2024-01-10",
			"touch_count": 1,
			"touches": [{
				"source": "crm",
				"date": "2024-01-10",
				"summary": "CRM record — status: Lost, value: $0",
				"type": "crm"
			}]
		}
	}
};
var recommendations_default = {
	generated_at: "2026-07-01T04:03:53.413155+00:00",
	summary: "Recommendations: 7 action(s) suggested; 3 high-priority, 4 medium-priority. Top: Prioritise: Database Setup.",
	counts: {
		"total": 7,
		"high": 3,
		"medium": 4
	},
	items: [
		{
			"category": "action",
			"title": "Prioritise: Database Setup",
			"rationale": "This item has a score of 90/100 in the action register.",
			"action": "Assign to Charlie and set a deadline today.",
			"priority": "high"
		},
		{
			"category": "crm",
			"title": "Re-engage Ross Law before it goes cold",
			"rationale": "This account scored 23/100 — risk bucket, Lost, contacted 903 day(s) ago, 0 related open item(s).",
			"action": "Send a personal touchpoint email and update the CRM last contact date.",
			"priority": "high"
		},
		{
			"category": "pipeline",
			"title": "Escalate TechInc — deal is slipping",
			"rationale": "This deal ($5,000) has a pipeline risk score of 99/100 (Qualified, touched 905 day(s) ago, 0 related open item(s)).",
			"action": "Reset the close plan, confirm stakeholder availability, and set a hard next-step date.",
			"priority": "high"
		},
		{
			"category": "crm",
			"title": "Expand TechInc while momentum is high",
			"rationale": "This account scored 82/100 — strong engagement, qualified status.",
			"action": "Propose an upsell or referral conversation while the relationship is warm.",
			"priority": "medium"
		},
		{
			"category": "pipeline",
			"title": "$7,500 in pipeline needs attention this week",
			"rationale": "2 deals are in risk or watch — combined value at risk.",
			"action": "Block time for a pipeline review; advance or close each deal this week.",
			"priority": "medium"
		},
		{
			"category": "kpi",
			"title": "KPI regression: high priority open is declining (latest 1, avg 0.8)",
			"rationale": "A key metric is trending in the wrong direction over the past two weeks.",
			"action": "Investigate the root cause and add a corrective action to this week's priorities.",
			"priority": "medium"
		},
		{
			"category": "kpi",
			"title": "KPI regression: stock alerts is declining (latest 1, avg 0.8)",
			"rationale": "A key metric is trending in the wrong direction over the past two weeks.",
			"action": "Investigate the root cause and add a corrective action to this week's priorities.",
			"priority": "medium"
		}
	]
};
var revenue_forecast_default = {
	generated_at: "2026-07-01T04:03:53.512925+00:00",
	summary: "Revenue forecast: 2 active deal(s), $7,500 total pipeline; 30d: $2,875 projected (2 deal(s)); 60d: $2,875 projected (2 deal(s)); 90d: $2,875 projected (2 deal(s)).",
	horizons: {
		"30": {
			"days": 30,
			"deal_count": 2,
			"projected_revenue": 2875,
			"best_case_revenue": 7500
		},
		"60": {
			"days": 60,
			"deal_count": 2,
			"projected_revenue": 2875,
			"best_case_revenue": 7500
		},
		"90": {
			"days": 90,
			"deal_count": 2,
			"projected_revenue": 2875,
			"best_case_revenue": 7500
		}
	},
	active_deals: [{
		"company": "TechInc",
		"lead_name": "John Doe",
		"status": "Qualified",
		"value": 5e3,
		"age_days": 907,
		"days_remaining": 1,
		"close_rate": .5,
		"expected_revenue": 2500
	}, {
		"company": "WebSoft",
		"lead_name": "Sara Smith",
		"status": "Contacted",
		"value": 2500,
		"age_days": 906,
		"days_remaining": 1,
		"close_rate": .15,
		"expected_revenue": 375
	}],
	total_pipeline: 7500,
	historical_close_rate: .5
};
var deal_progression_default = {
	generated_at: "2026-07-01T04:03:53.536640+00:00",
	summary: "Deal progression: 2 active deal(s); 2 stuck; 0 on track; oldest stuck: WebSoft (905d in 'Contacted').",
	counts: {
		"total": 2,
		"stuck": 2,
		"on_track": 0,
		"closed_lost": 1
	},
	items: [{
		"company": "WebSoft",
		"lead_name": "Sara Smith",
		"status": "Contacted",
		"lead_value": 2500,
		"age_days": 906,
		"days_since_contact": 905,
		"stage_threshold_days": 14,
		"stage_label": "stuck",
		"next_step": "Push out of 'contacted' — last touched 905d ago, threshold is 14d."
	}, {
		"company": "TechInc",
		"lead_name": "John Doe",
		"status": "Qualified",
		"lead_value": 5e3,
		"age_days": 907,
		"days_since_contact": 904,
		"stage_threshold_days": 30,
		"stage_label": "stuck",
		"next_step": "Push out of 'qualified' — last touched 904d ago, threshold is 30d."
	}]
};
var renewal_reminders_default = {
	generated_at: "2026-07-01T04:03:53.606175+00:00",
	summary: "Renewal reminders: 2 due in next 90d; 2 overdue; 0 this month; 0 upcoming; next: WebSoft (Overdue by 540d).",
	counts: {
		"total": 2,
		"overdue": 2,
		"this_month": 0,
		"upcoming": 0
	},
	items: [{
		"company": "WebSoft",
		"lead_name": "Sara Smith",
		"status": "Contacted",
		"lead_value": 2500,
		"renewal_date": "2025-01-06",
		"renewal_field": "estimated (last contact + 1yr)",
		"days_until": -540,
		"urgency": "overdue",
		"label": "Overdue by 540d",
		"next_step": "Renewal is overdue — reach out immediately to avoid lapse.",
		"last_contact": "2024-01-07"
	}, {
		"company": "TechInc",
		"lead_name": "John Doe",
		"status": "Qualified",
		"lead_value": 5e3,
		"renewal_date": "2025-01-07",
		"renewal_field": "estimated (last contact + 1yr)",
		"days_until": -539,
		"urgency": "overdue",
		"label": "Overdue by 539d",
		"next_step": "Renewal is overdue — reach out immediately to avoid lapse.",
		"last_contact": "2024-01-08"
	}],
	lookahead_days: 90
};
var weekly_digest_default = {
	generated_at: "2026-06-23T13:35:32.866697",
	days: [
		{
			"completed": 1,
			"high_open": 0,
			"stock_alerts": 0,
			"qualified": 1,
			"pipeline_value": 7500,
			"date": "2026-06-17"
		},
		{
			"completed": 1,
			"high_open": 1,
			"stock_alerts": 1,
			"qualified": 1,
			"pipeline_value": 7500,
			"date": "2026-06-22"
		},
		{
			"completed": 1,
			"high_open": 1,
			"stock_alerts": 1,
			"qualified": 1,
			"pipeline_value": 7500,
			"date": "2026-06-23"
		}
	],
	summary: {
		"avg_completed": 1,
		"avg_high_open": .7,
		"avg_stock_alerts": .7,
		"avg_qualified": 1,
		"avg_pipeline_value": 7500
	}
};
var actionRegister = action_register_default;
var followUpPlan = follow_up_plan_default;
var meetingExecution = meeting_execution_plan_default;
var customerHealth = customer_health_report_default;
var pipelineRisk = pipeline_risk_report_default;
var approvalWorkflow = approval_workflow_default;
var kpiDigest = kpi_digest_report_default;
var communicationTimeline = communication_timeline_default;
var recommendationsReport = recommendations_default;
var revenueForecast = revenue_forecast_default;
var dealProgression = deal_progression_default;
var renewalReminders = renewal_reminders_default;
var weeklyDigest = weekly_digest_default;
function money(value) {
	return `$${Number(value || 0).toLocaleString(void 0, { maximumFractionDigits: 0 })}`;
}
function safeText(value, fallback = "") {
	return String(value ?? "").trim() || fallback;
}
function toStatus(input) {
	const text = safeText(input).toLowerCase();
	if (text.includes("risk") || text === "blocked") return "risk";
	if (text.includes("watch") || text.includes("pending")) return "watch";
	return "healthy";
}
function toTrend(input) {
	const text = safeText(input).toLowerCase();
	if (text.includes("declin") || text === "down") return "down";
	if (text.includes("improv") || text === "up") return "up";
	return "flat";
}
var chCounts = customerHealth?.counts || {};
var prCounts = pipelineRisk?.counts || {};
var kpiFlags = kpiDigest?.flags || [];
var baseScore = 80;
var scorePenalty = Number(chCounts.risk || 0) * 8 + Number(prCounts.risk || 0) * 7 + kpiFlags.length * 2;
var dayScore = {
	score: Math.max(35, Math.min(96, baseScore - scorePenalty)),
	delta: Math.max(1, 6 - Math.min(5, kpiFlags.length)),
	pulse: safeText(recommendationsReport?.summary, "Daily intelligence generated from live operational signals."),
	readiness: [
		{
			label: "Pipeline Coverage",
			value: Number(revenueForecast?.total_pipeline || 0) / 1e3,
			status: Number(prCounts.risk || 0) > 0 ? "watch" : "healthy"
		},
		{
			label: "Forecast Confidence",
			value: Number(revenueForecast?.horizons?.["90"]?.projected_revenue || 0) > 0 ? .78 : .55,
			status: Number(prCounts.risk || 0) > 0 ? "watch" : "healthy"
		},
		{
			label: "Renewal Exposure",
			value: Number(renewalReminders?.counts?.overdue || 0) / Math.max(1, Number(renewalReminders?.counts?.total || 1)),
			status: Number(renewalReminders?.counts?.overdue || 0) > 0 ? "risk" : "healthy"
		},
		{
			label: "Open Approvals",
			value: Number(approvalWorkflow?.counts?.total_pending || 0),
			status: Number(approvalWorkflow?.counts?.total_pending || 0) > 0 ? "watch" : "healthy"
		}
	]
};
var actions = (actionRegister?.items || []).map((item, i) => ({
	id: `a${i + 1}`,
	title: safeText(item?.title, "Untitled action"),
	owner: safeText(item?.owner, "Unassigned"),
	due: safeText(item?.due_date, "No due date"),
	priority: Number(item?.score || 0) >= 85 ? "P0" : Number(item?.score || 0) >= 70 ? "P1" : "P2",
	status: toStatus(item?.priority || item?.reason)
}));
var followUps = (followUpPlan?.items || []).map((item, i) => ({
	id: `f${i + 1}`,
	contact: safeText(item?.owner, "Owner"),
	company: safeText(item?.title, "Account"),
	channel: safeText(item?.source).toLowerCase().includes("email") ? "Email" : safeText(item?.source).toLowerCase().includes("task") ? "Call" : "LinkedIn",
	draft: safeText(item?.nudge_body || item?.nudge_subject || item?.reason, "Follow-up needed"),
	scheduled: safeText(item?.due_date, "Queued")
}));
var meetings = (meetingExecution?.items || []).map((item, i) => ({
	id: `m${i + 1}`,
	title: safeText(item?.title, "Execution item"),
	attendees: [safeText(item?.owner, "Owner")],
	decisions: Math.max(1, Math.round(Number(item?.score || 50) / 40)),
	actions: 1,
	time: safeText(item?.due_date, "This week")
}));
var accountHealth = (customerHealth?.items || []).map((item) => ({
	account: safeText(item?.company, "Account"),
	arr: money(item?.lead_value),
	status: toStatus(item?.bucket),
	signal: safeText(item?.reason, "No signal"),
	owner: safeText(item?.lead_name, "Owner"),
	lastTouch: safeText(item?.status, "Unknown")
}));
var pipelineRisks = (pipelineRisk?.items || []).map((item) => ({
	deal: `${safeText(item?.company, "Deal")} - ${safeText(item?.status, "Stage")}`,
	stage: safeText(item?.status, "Unknown"),
	value: money(item?.lead_value),
	risk: toStatus(item?.bucket),
	reason: safeText(item?.reason, "No reason")
}));
var pending = Number(approvalWorkflow?.counts?.total_pending || 0);
var approved = Number(approvalWorkflow?.counts?.total_approved || 0);
var blocked = Number(approvalWorkflow?.counts?.total_rejected || 0);
var approvalItems = approvalWorkflow?.items || [];
var approvals = [...approvalItems.map((item, i) => ({
	id: safeText(item?.draft_id, `ap${i + 1}`),
	title: safeText(item?.subject, "Draft approval"),
	requester: safeText(item?.recipient, "Unknown"),
	amount: "-",
	age: safeText(item?.created_at, "now"),
	status: "Pending"
})), ...approvalItems.length === 0 ? [{
	id: "ap-pending",
	title: `Pending approvals: ${pending}`,
	requester: "Workflow",
	amount: "-",
	age: "live",
	status: pending > 0 ? "Pending" : approved > 0 ? "Approved" : blocked > 0 ? "Blocked" : "Approved"
}] : []];
var sentiment = (pipelineRisk?.items || []).map((item, i) => {
	const status = toStatus(item?.bucket);
	const score = status === "healthy" ? .5 : status === "watch" ? .1 : -.45;
	return {
		thread: safeText(item?.next_step, "Deal signal"),
		account: safeText(item?.company, "Account"),
		score,
		trend: status === "healthy" ? "up" : status === "watch" ? "flat" : "down",
		lastReply: safeText(item?.status, "recent")
	};
});
var recommendations = (recommendationsReport?.items || []).map((item, i) => ({
	id: `r${i + 1}`,
	title: safeText(item?.title, "Recommendation"),
	rationale: safeText(item?.rationale, "No rationale"),
	impact: safeText(item?.priority).toLowerCase() === "high" ? "High" : "Medium",
	effort: "Medium"
}));
var kpiMap = kpiDigest?.kpis || {};
var kpis = Object.keys(kpiMap).map((key) => {
	const row = kpiMap[key] || {};
	return {
		label: key.replace(/_/g, " ").replace(/\b\w/g, (m) => m.toUpperCase()),
		value: key.includes("value") ? money(row?.latest) : String(row?.latest ?? "-"),
		delta: `avg ${row?.avg ?? "-"}`,
		trend: toTrend(row?.trend),
		flag: toTrend(row?.trend) === "down" ? "watch" : void 0
	};
});
var timeline = Object.entries(communicationTimeline?.accounts || {}).flatMap(([company, account], idx) => (account?.touches || []).map((touch, j) => ({
	id: `t${idx + 1}-${j + 1}`,
	time: safeText(touch?.date, "--:--").slice(0, 10),
	type: safeText(touch?.source, "Note").toLowerCase().includes("email") ? "Email" : safeText(touch?.source).toLowerCase().includes("task") ? "Call" : safeText(touch?.source).toLowerCase().includes("meeting") ? "Meeting" : "Note",
	summary: safeText(touch?.summary, "No summary"),
	account: String(company)
}))).slice(0, 8);
var forecast = [
	"30",
	"60",
	"90"
].map((h) => {
	const row = revenueForecast?.horizons?.[h] || {};
	const projected = Number(row?.projected_revenue || 0);
	const best = Number(row?.best_case_revenue || 0);
	const confidence = best > 0 ? Math.min(1, projected / best + .25) : .5;
	return {
		window: `${h}d`,
		committed: money(projected),
		best: money(best),
		pipeline: money(revenueForecast?.total_pipeline || 0),
		confidence
	};
});
var deals = (dealProgression?.items || []).map((item) => ({
	name: safeText(item?.company, "Deal"),
	stage: safeText(item?.status, "Stage"),
	value: money(item?.lead_value),
	movement: safeText(item?.stage_label).toLowerCase() === "stuck" ? "stuck" : "on-track",
	days: Number(item?.days_since_contact || 0)
}));
var renewals = (renewalReminders?.items || []).map((item) => ({
	account: safeText(item?.company, "Account"),
	arr: money(item?.lead_value),
	date: safeText(item?.renewal_date, "Unknown"),
	bucket: safeText(item?.urgency, "upcoming") === "overdue" ? "overdue" : safeText(item?.urgency) === "this_month" ? "this-month" : "upcoming",
	owner: safeText(item?.lead_name, "Owner")
}));
var weekly = (weeklyDigest?.days || []).map((row, i) => {
	const completed = Number(row?.completed || 0);
	const highOpen = Number(row?.high_open || 0);
	const qualified = Number(row?.qualified || 0);
	const attainment = Math.max(.5, Math.min(1.2, completed / Math.max(1, highOpen + 1)));
	return {
		rep: safeText(row?.date, `Day ${i + 1}`),
		meetings: completed + highOpen,
		pipeline: money(row?.pipeline_value || 0),
		won: money(qualified * 1e3),
		attainment
	};
});
var surfaces = [
	{
		name: "Daily Executive Briefing",
		href: "/executive_briefing.html",
		status: "healthy",
		updated: safeText(actionRegister?.generated_at, "recent")
	},
	{
		name: "Account Health Radar",
		href: "#health",
		status: Number(customerHealth?.counts?.risk || 0) > 0 ? "watch" : "healthy",
		updated: safeText(customerHealth?.generated_at, "recent")
	},
	{
		name: "Renewal Save Plays",
		href: "#renewals",
		status: Number(renewalReminders?.counts?.overdue || 0) > 0 ? "risk" : "healthy",
		updated: safeText(renewalReminders?.generated_at, "recent")
	},
	{
		name: "Forecast Workbook",
		href: "#forecast",
		status: Number(pipelineRisk?.counts?.risk || 0) > 0 ? "watch" : "healthy",
		updated: safeText(revenueForecast?.generated_at, "recent")
	}
];
var briefing = {
	headline: safeText(recommendationsReport?.summary, "Daily briefing generated from live operational data."),
	bullets: [
		safeText(actionRegister?.summary, "Action register updated."),
		safeText(pipelineRisk?.summary, "Pipeline risk reviewed."),
		safeText(customerHealth?.summary, "Customer health scored.")
	],
	prepared: `Prepared from live artifacts \u00b7 ${safeText(actionRegister?.generated_at, "now")}`
};
//#endregion
export { weekly as _, dayScore as a, forecast as c, pipelineRisks as d, recommendations as f, timeline as g, surfaces as h, briefing as i, kpis as l, sentiment as m, actions as n, deals as o, renewals as p, approvals as r, followUps as s, accountHealth as t, meetings as u };
