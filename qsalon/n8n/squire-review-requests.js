import { workflow, node, trigger, expr, ifElse } from '@n8n/workflow-sdk';

const BOOK_TBL = { __rl: true, mode: 'id', value: '1b54l7aAwCRz45S5', cachedResultName: 'qsalon_squire_bookings' };
const REQ_TBL = { __rl: true, mode: 'id', value: '7sKADJPBdl6F7w38', cachedResultName: 'qsalon_review_requests' };
const GMAIL = { gmailOAuth2: { id: 'y24x7BiqwhsuUuFf', name: 'Gmail account 4' } };

const every15 = trigger({ type: 'n8n-nodes-base.scheduleTrigger', version: 1.3, config: { name: 'Every 15 min, 7 AM–9 PM ET', parameters: { rule: { interval: [{ field: 'cronExpression', expression: '*/15 7-21 * * *' }] } } } });

// ---------- Branch A: read SQUIRE emails in info@ and log bookings ----------
const getEmails = node({ type: 'n8n-nodes-base.gmail', version: 2.2, config: { name: 'SQUIRE Emails (last 21 days)', parameters: {
  resource: 'message', operation: 'getAll', returnAll: false, limit: 100, simple: false,
  filters: { q: 'from:info@getsquire.com newer_than:21d', readStatus: 'both' }, options: {} }, credentials: GMAIL } });

const parse = node({ type: 'n8n-nodes-base.code', version: 2, config: { name: 'Parse SQUIRE Emails', parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `
const out = [];
const strip = h => String(h || '').replace(/<style[\\s\\S]*?<\\/style>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/\\s+/g, ' ');
for (const it of $input.all()) {
  const j = it.json || {};
  const subject = String(j.subject || '');
  const text = String(j.text || '');
  const flat = strip(j.html) + ' ' + text.replace(/\\s+/g, ' ');
  const code = (text.match(/Confirmation code:\\s*([A-Z0-9]+)/i) || [])[1] || '';
  if (!code) continue;
  const isCancel = /cancel/i.test(subject);
  const isNew = /has a new/i.test(subject);
  if (!isCancel && !isNew) continue;
  const name = ((text.match(/Client:\\s*(.+)/i) || [])[1] || '').trim();
  const email = ((text.match(/Email:\\s*([^\\s]+@[^\\s]+)/i) || [])[1] || '').trim().toLowerCase();
  const phone = ((text.match(/Phone:\\s*(\\+?[0-9]+)/i) || [])[1] || '').trim();
  const service = ((text.match(/Service:\\s*(.+)/i) || [])[1] || '').trim();
  const dm = text.match(/Duration:\\s*(?:(\\d+)\\s*hours?)?\\s*(?:(\\d+)\\s*min)?/i) || [];
  let minutes = (parseInt(dm[1] || '0', 10) * 60) + parseInt(dm[2] || '0', 10);
  if (!minutes) minutes = 60;
  const tm = flat.match(/(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,\\s*([A-Z][a-z]{2})[a-z]*\\s+(\\d{1,2})(?:st|nd|rd|th)?,\\s*(\\d{1,2}:\\d{2}\\s*[AP]M)/);
  let apptAt = null;
  if (tm) {
    const sent = DateTime.fromISO(String(j.date || new Date().toISOString())).setZone('America/New_York');
    let dt = DateTime.fromFormat(tm[1] + ' ' + tm[2] + ' ' + sent.year + ' ' + tm[3].replace(/\\s+/, ' ').toUpperCase(), 'LLL d yyyy h:mm a', { zone: 'America/New_York' });
    if (dt.isValid && dt < sent.minus({ days: 2 })) dt = dt.plus({ years: 1 });
    if (dt.isValid) apptAt = dt;
  }
  const first = (name.split(/\\s+/)[0] || '').replace(/^./, c => c.toUpperCase());
  out.push({ json: { kind: isCancel ? 'cancel' : 'new', code, clientName: name, firstName: first, email: /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email) ? email : '', phone, service,
    apptAt: apptAt ? apptAt.toUTC().toISO() : null, sendAt: apptAt ? apptAt.plus({ minutes: minutes + 60 }).toUTC().toISO() : null, gmailId: j.id || '' } });
}
return out;` } } });

const loadBookings = node({ type: 'n8n-nodes-base.dataTable', version: 1.1, config: { name: 'Load Logged Bookings', executeOnce: true, alwaysOutputData: true, parameters: { resource: 'row', operation: 'get', dataTableId: BOOK_TBL, returnAll: true } } });

const diff = node({ type: 'n8n-nodes-base.code', version: 2, config: { name: 'New or Canceled?', parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `
const logged = {};
for (const r of $input.all()) { const j = r.json || {}; if (j.code) logged[j.code] = j; }
const out = [];
const seen = {};
for (const it of $('Parse SQUIRE Emails').all()) {
  const p = it.json;
  if (p.kind === 'new') {
    if (logged[p.code] || seen[p.code] || !p.apptAt) continue;
    seen[p.code] = true;
    out.push({ json: Object.assign({ action: 'insert' }, p) });
  } else if (p.kind === 'cancel' && logged[p.code] && logged[p.code].status === 'scheduled') {
    out.push({ json: { action: 'cancel', rowId: logged[p.code].id, code: p.code } });
  }
}
return out;` } } });

const isInsert = ifElse({ version: 2.2, config: { name: 'New Booking?', parameters: { conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' },
  conditions: [{ leftValue: expr('{{ $json.action }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'insert' }], combinator: 'and' } } } });

const insertBooking = node({ type: 'n8n-nodes-base.dataTable', version: 1.1, config: { name: 'Log Booking', parameters: { resource: 'row', operation: 'insert', dataTableId: BOOK_TBL,
  columns: { mappingMode: 'defineBelow', value: {
    code: expr('{{ $json.code }}'), clientName: expr('{{ $json.clientName }}'), firstName: expr('{{ $json.firstName }}'), email: expr('{{ $json.email }}'),
    phone: expr('{{ $json.phone }}'), service: expr('{{ $json.service }}'), apptAt: expr('{{ $json.apptAt }}'), sendAt: expr('{{ $json.sendAt }}'),
    status: 'scheduled', gmailId: expr('{{ $json.gmailId }}') } } } } });

const cancelBooking = node({ type: 'n8n-nodes-base.dataTable', version: 1.1, config: { name: 'Mark Canceled', parameters: { resource: 'row', operation: 'update', dataTableId: BOOK_TBL,
  matchType: 'allConditions', filters: { conditions: [{ keyName: 'id', condition: 'eq', keyValue: expr('{{ $json.rowId }}') }] },
  columns: { mappingMode: 'defineBelow', value: { status: 'canceled', notes: 'SQUIRE cancellation email' } } } } });

// ---------- Branch B: send review emails that are due ----------
const loadScheduled = node({ type: 'n8n-nodes-base.dataTable', version: 1.1, config: { name: 'Load Scheduled Bookings', parameters: { resource: 'row', operation: 'get', dataTableId: BOOK_TBL,
  matchType: 'allConditions', filters: { conditions: [{ keyName: 'status', condition: 'eq', keyValue: 'scheduled' }] }, returnAll: true } } });

const loadAsked = node({ type: 'n8n-nodes-base.dataTable', version: 1.1, config: { name: 'Load Past Review Requests', executeOnce: true, alwaysOutputData: true, parameters: { resource: 'row', operation: 'get', dataTableId: REQ_TBL, returnAll: true } } });

const due = node({ type: 'n8n-nodes-base.code', version: 2, config: { name: 'Due Now?', parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `
const now = Date.now();
const CATCH_UP_DAYS = 10; // appointments older than this are never emailed
const asked = {};
for (const r of $input.all()) { const j = r.json || {}; if ((j.status === 'sent' || j.status === 'pending') && j.email) asked[String(j.email).toLowerCase()] = true; }
const out = [];
const thisRun = {};
for (const it of $('Load Scheduled Bookings').all()) {
  const b = it.json;
  const t = Date.parse(b.sendAt);
  if (!b.email || Number.isNaN(t) || t > now) continue;
  if (now - t > CATCH_UP_DAYS * 86400000) continue;
  const key = String(b.email).toLowerCase();
  if (asked[key] || thisRun[key]) continue;
  thisRun[key] = true;
  out.push({ json: { rowId: b.id, email: key, firstName: b.firstName || 'there', lastName: String(b.clientName || '').split(/\\s+/).slice(1).join(' '), phone: b.phone || '', service: b.service || '', code: b.code } });
}
return out;` } } });

const send = node({ type: 'n8n-nodes-base.gmail', version: 2.2, config: { name: 'Email Review Request', parameters: {
  resource: 'message', operation: 'send', sendTo: expr('{{ $json.email }}'),
  subject: 'The Q Salon for Men would love your feedback', emailType: 'html',
  message: expr('<div style="background:#f3f0ea;padding:32px 16px;font-family:Georgia,\'Times New Roman\',serif;color:#14202e"><div style="max-width:520px;margin:0 auto;background:#ffffff;border-top:4px solid #d6b984"><div style="background:#14202e;padding:26px 32px;text-align:center"><div style="font-size:22px;letter-spacing:4px;color:#f3f0ea">THE Q SALON</div><div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:4px;color:#d6b984;margin-top:6px">FOR MEN &middot; SARASOTA</div></div><div style="padding:32px;font-size:17px;line-height:1.6"><p style="margin:0 0 16px">Hi {{ $json.firstName }},</p><p style="margin:0 0 16px">Thank you for coming in. The Q Salon for Men would love your feedback.</p><p style="margin:0 0 24px">If you have a minute, please post a review to our Google profile. For a one-chair salon, every review means a lot, and it\'s how most men in Sarasota find us.</p><div style="text-align:center;margin:0 0 28px"><a href="https://g.page/r/Cfc4zlSjpFpJEBE/review" style="display:inline-block;background:#d6b984;color:#14202e;text-decoration:none;font-family:Arial,sans-serif;font-weight:bold;font-size:16px;padding:15px 34px;border-radius:999px">Post a review</a></div><p style="margin:0 0 4px">Thank you, truly.</p><p style="margin:0;font-size:20px">Susy</p><p style="margin:0;font-family:Arial,sans-serif;font-size:13px;color:#6b7280">Master barber &amp; stylist, The Q Salon for Men</p></div><div style="border-top:1px solid #ece6da;padding:18px 32px;font-family:Arial,sans-serif;font-size:13px;color:#6b7280;text-align:center">Ready for your next visit? <a href="https://theqsalonsrq.com/book" style="color:#14202e">Book your experience</a></div></div></div>'),
  options: { appendAttribution: false, senderName: 'Susy at The Q Salon for Men' } }, credentials: GMAIL } });

const markSent = node({ type: 'n8n-nodes-base.dataTable', version: 1.1, config: { name: 'Mark Booking Sent', parameters: { resource: 'row', operation: 'update', dataTableId: BOOK_TBL,
  matchType: 'allConditions', filters: { conditions: [{ keyName: 'id', condition: 'eq', keyValue: expr('{{ $(\'Due Now?\').item.json.rowId }}') }] },
  columns: { mappingMode: 'defineBelow', value: { status: 'sent', sentAt: expr('{{ $now.toISO() }}') } } } } });

const logReq = node({ type: 'n8n-nodes-base.dataTable', version: 1.1, config: { name: 'Log in Review Requests', parameters: { resource: 'row', operation: 'insert', dataTableId: REQ_TBL,
  columns: { mappingMode: 'defineBelow', value: {
    firstName: expr('{{ $(\'Due Now?\').item.json.firstName }}'), lastName: expr('{{ $(\'Due Now?\').item.json.lastName }}'), email: expr('{{ $(\'Due Now?\').item.json.email }}'),
    phone: expr('{{ $(\'Due Now?\').item.json.phone }}'), service: expr('{{ $(\'Due Now?\').item.json.service }}'), status: 'sent', channel: 'email',
    submittedAt: expr('{{ $now.toISO() }}'), sentAt: expr('{{ $now.toISO() }}'), notes: expr('SQUIRE {{ $(\'Due Now?\').item.json.code }}') } } } } });

export default workflow('qsalon-squire-reviews', 'Q Salon — SQUIRE Booking Review Requests')
  .add(every15).to(getEmails).to(parse).to(loadBookings).to(diff).to(isInsert.onTrue(insertBooking).onFalse(cancelBooking))
  .add(every15).to(loadScheduled).to(loadAsked).to(due).to(send).to(markSent).to(logReq);
