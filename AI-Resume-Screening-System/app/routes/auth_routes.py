# ============================================================
#  TalentSync — Auth Routes  (Blueprint: /api/auth)
# ============================================================

import os, random, smtplib, string
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, request, jsonify, session
from app.controllers.auth_controller import login_user, register_user
from app.database.connection import get_db
from app.utils.security import login_required
from app import limiter

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ── helpers ──────────────────────────────────────────────────
def _generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


# ── HTML Assets (Email Safe, inline SVG tables) ───────────────

# HireAI logo mark — white "H" on gradient background
_LOGO_SVG = """
<table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto 6px;">
  <tr>
    <td width="52" height="52" align="center" valign="middle"
        style="background:linear-gradient(135deg,#0f4fc5 0%,#6d28d9 100%);
               border-radius:14px;mso-border-radius:14px;">
      <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
        <tr>
          <td align="center" valign="middle"
              style="font-family:'Arial Black',Arial,sans-serif;font-size:24px;
                     font-weight:900;color:#ffffff;line-height:52px;
                     letter-spacing:-1px;mso-line-height-rule:exactly;
                     width:52px;height:52px;">H</td>
        </tr>
      </table>
    </td>
    <td width="8"></td>
    <td valign="middle"
        style="font-family:'Arial Black',Arial,sans-serif;font-size:19px;
               font-weight:900;color:#ffffff;letter-spacing:-0.5px;">
      HireAI
    </td>
  </tr>
</table>
"""

# Shield icon — inline SVG table cell (security / OTP)
_ICON_SHIELD = """
<table cellpadding="0" cellspacing="0" border="0" style="display:inline-table;vertical-align:middle;margin-right:8px;">
  <tr>
    <td width="18" height="18" align="center" valign="middle">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1260cc" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      </svg>
    </td>
  </tr>
</table>"""

# Clock icon — inline SVG (expires timer)
_ICON_CLOCK = """
<table cellpadding="0" cellspacing="0" border="0" style="display:inline-table;vertical-align:middle;margin-right:6px;">
  <tr>
    <td width="16" height="16" align="center" valign="middle">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12 6 12 12 16 14"/>
      </svg>
    </td>
  </tr>
</table>"""

# Checkmark icon — inline SVG (success / welcome)
_ICON_CHECK = """
<table cellpadding="0" cellspacing="0" border="0" style="display:inline-table;vertical-align:middle;margin-right:8px;">
  <tr>
    <td width="18" height="18" align="center" valign="middle"
        style="background:#d1fae5;border-radius:50%;">
      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
    </td>
  </tr>
</table>"""

# Warning / alert icon — inline SVG
_ICON_WARNING = """
<table cellpadding="0" cellspacing="0" border="0" style="display:inline-table;vertical-align:middle;margin-right:8px;">
  <tr>
    <td width="18" height="18" align="center" valign="middle"
        style="background:#fef3c7;border-radius:50%;">
      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#b45309" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
        <line x1="12" y1="9" x2="12" y2="13"/>
        <line x1="12" y1="17" x2="12.01" y2="17"/>
      </svg>
    </td>
  </tr>
</table>"""

# Feature icons for welcome email (briefcase, star, zap)
_ICON_BRIEFCASE = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1260cc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/></svg>"""
_ICON_STAR     = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>"""
_ICON_ZAP      = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>"""
_FEATURE_ICONS = [_ICON_BRIEFCASE, _ICON_STAR, _ICON_ZAP]


# ── Email base builder ────────────────────────────────────────
def _build_email_html(*, first_name: str, header_html: str,
                      body_html: str, footer_note: str = '') -> str:
    """Assembles a world-class responsive HTML email."""
    year = datetime.utcnow().year
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>HireAI</title>
  <!--[if mso]>
  <noscript><xml><o:OfficeDocumentSettings>
    <o:PixelsPerInch>96</o:PixelsPerInch>
  </o:OfficeDocumentSettings></xml></noscript>
  <![endif]-->
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    body {{ margin:0; padding:0; background:#eef2f7; -webkit-font-smoothing:antialiased; }}
    @media only screen and (max-width:600px) {{
      .email-card {{ width:100% !important; border-radius:0 !important; }}
      .email-body {{ padding:28px 20px !important; }}
      .otp-digit {{ width:36px !important; height:48px !important; font-size:26px !important; line-height:48px !important; }}
    }}
  </style>
</head>
<body style="margin:0;padding:0;background:#eef2f7;font-family:'Inter',Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background:#eef2f7;padding:40px 16px;">
  <tr><td align="center">

    <!-- Top wordmark bar -->
    <table width="560" cellpadding="0" cellspacing="0" border="0" class="email-card">
      <tr>
        <td style="padding-bottom:18px;text-align:center;">
          <span style="font-family:'Inter',Arial,sans-serif;font-size:11px;font-weight:700;
                       color:#94a3b8;letter-spacing:0.12em;text-transform:uppercase;">
            HIREAI &nbsp;&bull;&nbsp; AI-POWERED RECRUITMENT
          </span>
        </td>
      </tr>
    </table>

    <!-- Main card -->
    <table width="560" cellpadding="0" cellspacing="0" border="0" class="email-card"
           style="background:#ffffff;border-radius:20px;
                  box-shadow:0 2px 4px rgba(0,0,0,0.03),0 8px 32px rgba(15,47,197,0.10);
                  overflow:hidden;">

      <!-- ── Gradient Header ── -->
      <tr>
        <td style="background:linear-gradient(135deg,#0f2fb5 0%,#3b1fa8 50%,#5b1fbd 100%);
                   padding:36px 44px 34px;text-align:center;">
          {header_html}
        </td>
      </tr>

      <!-- ── Body ── -->
      <tr>
        <td class="email-body" style="padding:40px 48px 32px;">
          <p style="margin:0 0 6px;font-size:18px;font-weight:700;color:#0f172a;letter-spacing:-0.2px;">
            Hi {first_name},
          </p>
          {body_html}
        </td>
      </tr>

      <!-- ── Thin gradient divider ── -->
      <tr>
        <td style="padding:0 48px;">
          <div style="height:1px;background:linear-gradient(90deg,transparent,#dde3ef 20%,#dde3ef 80%,transparent);"></div>
        </td>
      </tr>

      <!-- ── Footer inside card ── -->
      <tr>
        <td style="padding:22px 48px 32px;text-align:center;">
          {f'<p style="margin:0 0 10px;font-size:12px;color:#94a3b8;line-height:1.7;">{footer_note}</p>' if footer_note else ''}
          <p style="margin:0;font-size:12px;color:#b0bac6;">
            &copy; {year} HireAI &nbsp;&middot;&nbsp;
            <a href="mailto:hetsony143@gmail.com" style="color:#6d82a8;text-decoration:none;">Support</a>
            &nbsp;&middot;&nbsp;
            <a href="#" style="color:#6d82a8;text-decoration:none;">Privacy Policy</a>
          </p>
        </td>
      </tr>

    </table>

    <!-- Below-card fine print -->
    <table width="560" cellpadding="0" cellspacing="0" border="0" class="email-card">
      <tr>
        <td style="padding-top:18px;text-align:center;">
          <p style="margin:0;font-size:11px;color:#9aaab6;line-height:1.6;">
            This email was sent by HireAI. If you have questions, contact&nbsp;
            <a href="mailto:hetsony143@gmail.com"
            style="color:#6d82a8;text-decoration:none;">hetsony143@gmail.com</a>
          </p>
        </td>
      </tr>
    </table>

  </td></tr>
</table>
</body>
</html>"""


# ── Email: OTP (password reset / register verify) ─────────────
def _build_otp_email_html(first_name: str, otp: str,
                           purpose: str = 'reset') -> str:
    """Builds the OTP email for password-reset or registration verify."""
    is_register = purpose == 'register'
    action_verb = 'verify your email address' if is_register else 'reset your password'
    action_desc = (
        'Complete your HireAI registration by verifying your email.'
        if is_register else
        'We received a request to reset your HireAI account password.'
    )
    header_label = 'Email Verification' if is_register else 'Password Reset'

    # Header icon: lock for reset, envelope-check for register
    if is_register:
        header_icon_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"
             fill="none" stroke="rgba(255,255,255,0.95)" stroke-width="1.8"
             stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
          <polyline points="22,6 12,13 2,6"/>
        </svg>"""
    else:
        header_icon_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24"
             fill="none" stroke="rgba(255,255,255,0.95)" stroke-width="1.8"
             stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>"""

    # Render each OTP digit as a separate styled box
    digit_boxes = ''.join([
        f'<td style="padding:0 3px;">'
        f'<div style="width:46px;height:60px;background:#f0f5ff;border:2px solid #c7d7f9;'
        f'border-radius:12px;display:inline-block;line-height:60px;text-align:center;'
        f'font-family:\'Courier New\',monospace;font-size:32px;font-weight:900;'
        f'color:#0f2fb5;letter-spacing:0;">{d}</div>'
        f'</td>'
        for d in otp
    ])

    header_html = f"""
      <!-- Logo -->
      <div style="margin-bottom:22px;">{_LOGO_SVG}</div>

      <!-- Icon badge — table-based so SVG centers properly -->
      <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto 14px;">
        <tr>
          <td width="56" height="56" align="center" valign="middle"
              style="width:56px;height:56px;
                     background:rgba(255,255,255,0.15);border-radius:16px;
                     border:1px solid rgba(255,255,255,0.25);
                     text-align:center;vertical-align:middle;">
            {header_icon_svg}
          </td>
        </tr>
      </table>

      <div style="color:rgba(255,255,255,0.6);font-size:10px;font-weight:700;
                  letter-spacing:0.18em;text-transform:uppercase;margin-bottom:6px;">
        {header_label}
      </div>
      <div style="color:#ffffff;font-size:25px;font-weight:800;letter-spacing:-0.5px;">
        Your Secure Code
      </div>
      <div style="color:rgba(255,255,255,0.55);font-size:13px;margin-top:6px;">
        HireAI &middot; AI Recruitment Platform
      </div>
    """

    body_html = f"""
      <p style="margin:0 0 22px;font-size:15px;color:#475569;line-height:1.75;">
        {action_desc} Use the secure one-time code below &mdash; it
        <strong style="color:#0f172a;">expires in 10 minutes</strong> and
        can only be used once.
      </p>

      <!-- Security context box -->
      <table cellpadding="0" cellspacing="0" border="0" width="100%"
             style="background:#f0f5ff;border-left:3px solid #1260cc;
                    border-radius:0 8px 8px 0;margin-bottom:28px;">
        <tr>
          <td style="padding:12px 16px;">
            <table cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td valign="middle" style="padding-right:10px;">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                       fill="none" stroke="#1260cc" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  </svg>
                </td>
                <td valign="middle">
                  <span style="font-size:13px;color:#334155;line-height:1.5;">
                    <strong style="color:#1260cc;">Secure action requested</strong>
                    &nbsp;&mdash;&nbsp;to {action_verb}
                  </span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <!-- OTP digit boxes -->
      <div style="text-align:center;margin-bottom:28px;">
        <p style="margin:0 0 16px;font-size:10px;font-weight:700;letter-spacing:0.14em;
                  color:#94a3b8;text-transform:uppercase;">
          One-Time Password
        </p>
        <table cellpadding="0" cellspacing="0" border="0"
               style="margin:0 auto;border-collapse:separate;">
          <tr>{digit_boxes}</tr>
        </table>
        <p style="margin:16px 0 0;font-size:12px;color:#94a3b8;">
          <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
            <tr>
              <td valign="middle" style="padding-right:5px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24"
                     fill="none" stroke="#94a3b8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                </svg>
              </td>
              <td valign="middle" style="font-size:12px;color:#94a3b8;">
                Expires in <strong style="color:#64748b;">10 minutes</strong>
              </td>
            </tr>
          </table>
        </p>
      </div>

      <!-- Warning notice -->
      <table cellpadding="0" cellspacing="0" border="0" width="100%"
             style="background:#fffbeb;border:1px solid #fde68a;border-radius:12px;margin-bottom:10px;">
        <tr>
          <td style="padding:14px 18px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td width="26" valign="top" style="padding-right:10px;padding-top:1px;">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                       fill="none" stroke="#b45309" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                    <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                </td>
                <td valign="top">
                  <p style="margin:0;font-size:13px;color:#92400e;line-height:1.6;">
                    <strong>Security tip:</strong> HireAI will never ask for this code over
                    the phone or chat. Do not share it with anyone.
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <p style="margin:20px 0 0;font-size:13px;color:#94a3b8;line-height:1.7;">
        If you didn't request this, you can safely ignore this email.
        No changes will be made to your account.
      </p>
    """

    footer = (
        'This verification code was requested for your HireAI account registration.'
        if is_register else
        'This reset was triggered from the HireAI login page.'
    )

    return _build_email_html(
        first_name=first_name,
        header_html=header_html,
        body_html=body_html,
        footer_note=footer
    )


# ── Email: Welcome (after registration) ──────────────────────
def _build_welcome_email_html(first_name: str, role: str) -> str:
    role_label = 'HR Admin' if role == 'hr' else 'Candidate'
    role_features = (
        [
            ('Manage Job Postings', 'Post and track roles in seconds'),
            ('AI Candidate Ranking', 'Smart ATS scoring for every applicant'),
            ('Bulk Resume Analysis', 'Screen 100s of resumes automatically'),
        ] if role == 'hr' else [
        ('AI Resume Analysis', 'Get your ATS score and improve your resume'),
        ('Smart Job Matching', 'Find roles perfectly matched to your skills'),
        ('Real-time Insights', 'Track application status and skill gaps'),
    ])

    feature_rows = ''
    for svg_icon, (title, desc) in zip(_FEATURE_ICONS, role_features):
        feature_rows += f"""
        <tr>
          <td style="padding:0 0 16px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td width="44" style="vertical-align:top;padding-right:14px;">
                  <div style="width:42px;height:42px;border-radius:12px;
                              background:#f1f5ff;border:1px solid #e0e7ff;
                              text-align:center;line-height:42px;display:inline-block;">
                    {svg_icon}
                  </div>
                </td>
                <td style="vertical-align:middle;">
                  <p style="margin:0 0 2px;font-size:14px;font-weight:700;
                            color:#0f172a;">{title}</p>
                  <p style="margin:0;font-size:13px;color:#64748b;line-height:1.5;">{desc}</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>"""

    header_html = f"""
      {_LOGO_SVG}
      <div style="margin-top:18px;">
        <div style="display:inline-block;background:rgba(16,185,129,0.22);
                    border:1px solid rgba(16,185,129,0.45);border-radius:999px;
                    padding:4px 14px;margin-bottom:12px;">
          <span style="color:#a7f3d0;font-size:11px;font-weight:700;
                       letter-spacing:0.10em;">&#10003; ACCOUNT ACTIVATED</span>
        </div>
        <div style="color:#ffffff;font-size:25px;font-weight:800;
                    letter-spacing:-0.5px;margin-bottom:6px;">
          Welcome aboard, {first_name}!
        </div>
        <div style="color:rgba(255,255,255,0.58);font-size:13px;">
          Your {role_label} account is ready to use
        </div>
      </div>
    """

    body_html = f"""
      <p style="margin:0 0 24px;font-size:15px;color:#475569;line-height:1.75;">
        Your HireAI account has been successfully created and your
        email is verified. Here&rsquo;s what you can do right now:
      </p>

      <!-- Features list -->
      <div style="background:#f8fafc;border-radius:14px;border:1px solid #e8eef6;
                  padding:22px 22px 6px;margin-bottom:28px;">
        <table cellpadding="0" cellspacing="0" border="0" width="100%">
          {feature_rows}
        </table>
      </div>

      <!-- CTA Button -->
      <div style="text-align:center;margin-bottom:28px;">
        <a href="http://localhost:5050" target="_blank"
           style="display:inline-block;background:linear-gradient(135deg,#0f2fb5,#5b1fbd);
                  color:#ffffff;font-size:15px;font-weight:700;padding:14px 38px;
                  border-radius:12px;text-decoration:none;letter-spacing:0.02em;
                  box-shadow:0 4px 16px rgba(15,47,181,0.35);">
          Open HireAI Dashboard &rarr;
        </a>
      </div>

      <!-- Success row -->
      <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
        <tr>
          <td valign="middle" style="padding-right:8px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                 fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </td>
          <td valign="middle" style="font-size:13px;color:#10b981;font-weight:600;">
            Email verified &amp; account active
          </td>
        </tr>
      </table>
    """

    return _build_email_html(
        first_name=first_name,
        header_html=header_html,
        body_html=body_html,
        footer_note='You are receiving this because you created a HireAI account.'
    )


# ── SMTP dispatcher ───────────────────────────────────────────
def _dispatch_email(to_email: str, subject: str, html_body: str) -> bool:
    """Send an HTML email via Gmail SMTP. Returns True on success."""
    sender  = os.getenv('MAIL_SENDER', '')
    app_pwd = os.getenv('MAIL_APP_PASSWORD', '')

    if not sender or not app_pwd or sender == 'your_gmail@gmail.com':
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject']  = subject
    msg['From']     = f'HireAI <{sender}>'
    msg['To']       = to_email
    msg['Reply-To'] = f'HireAI Support <{sender}>'
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=12) as server:
            server.login(sender, app_pwd)
            server.sendmail(sender, to_email, msg.as_string())
        return True
    except Exception as exc:
        print(f'[Email error → {to_email}] {exc}')
        return False



# ── Public helpers ────────────────────────────────────────────
def _send_otp_email(to_email: str, otp: str,
                    user_name: str = '', purpose: str = 'reset') -> bool:
    first_name = (user_name.split()[0] if user_name else 'there').capitalize()
    if purpose == 'register':
        subject = f'[{otp}] Verify your TalentSync email'
    else:
        subject = f'[{otp}] Reset your TalentSync password'
    html = _build_otp_email_html(first_name, otp, purpose)
    return _dispatch_email(to_email, subject, html)


def _send_welcome_email(to_email: str, user_name: str, role: str) -> bool:
    first_name = (user_name.split()[0] if user_name else 'there').capitalize()
    subject    = f'Welcome to TalentSync, {first_name}! Your account is ready'
    html       = _build_welcome_email_html(first_name, role)
    return _dispatch_email(to_email, subject, html)


# ── Routes ───────────────────────────────────────────────────

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Max 5 login attempts per minute per IP
def login():
    """POST /api/auth/login  →  { email, password }
    Only registered, email-verified accounts can log in.
    """
    data     = request.get_json(silent=True) or {}
    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'}), 400

    # Block login for unregistered emails immediately (prevents enumeration via timing)
    with get_db() as conn:
        user_row = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
    if not user_row:
        return jsonify({'success': False, 'message': 'No account found with that email. Please register first.'}), 401

    result = login_user(email, password)
    if result.get('success'):
        session.clear()  # Regenerate session on login (session fixation prevention)
        session['user_id'] = result['user']['id']
    return jsonify(result)


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("3 per minute")
def register():
    """POST /api/auth/register  →  { name, email, password, role }
    Requires email_verified session token set by /verify_register_otp.
    """
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()

    # Enforce that OTP was verified for this exact email
    verified = session.get('reg_verified_email')
    if not verified or verified != email:
        return jsonify({
            'success': False,
            'message': 'Email not verified. Please complete OTP verification first.'
        }), 403

    result = register_user(
        data.get('name', ''),
        email,
        data.get('password', ''),
        data.get('role', 'candidate')
    )
    if result.get('success'):
        session.clear()
        session['user_id'] = result['user']['id']
    return jsonify(result)


# ── Registration OTP — Step 1: Send OTP ──────────────────────
@auth_bp.route('/send_register_otp', methods=['POST'])
@limiter.limit("3 per minute")
def send_register_otp():
    """
    POST /api/auth/send_register_otp  →  { email }
    Validates the email is not already registered, then sends a 6-digit OTP.
    """
    data  = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'success': False, 'message': 'Email is required.'}), 400

    # Block if already registered
    with get_db() as conn:
        existing = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
    if existing:
        return jsonify({
            'success': False,
            'message': 'An account with this email already exists. Please log in instead.'
        }), 409

    otp        = _generate_otp()
    expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    name       = data.get('name', '')

    # Invalidate old OTPs for this email
    with get_db() as conn:
        conn.execute("UPDATE password_reset_otps SET used=1 WHERE email=? AND used=0", (email,))
        conn.execute(
            "INSERT INTO password_reset_otps (email, otp, expires_at, used) VALUES (?,?,?,0)",
            (email, otp, expires_at)
        )
        conn.commit()

    sent = _send_otp_email(email, otp, name, purpose='register')

    if sent:
        return jsonify({
            'success': True,
            'message': f'Verification OTP sent to {email}. Check your inbox.'
        })
    else:
        return jsonify({
            'success': True,
            'dev_otp': otp,
            'message': f'Dev mode: Email not configured. OTP is {otp}'
        })


# ── Registration OTP — Step 2: Verify OTP & Create Account ───
@auth_bp.route('/verify_register_otp', methods=['POST'])
@limiter.limit("5 per minute")
def verify_register_otp():
    """
    POST /api/auth/verify_register_otp  →  { email, otp, name, password, role }
    Verifies OTP, then creates the account immediately.
    """
    data     = request.get_json(silent=True) or {}
    email    = data.get('email', '').strip().lower()
    otp      = data.get('otp', '').strip()
    name     = data.get('name', '').strip()
    password = data.get('password', '')
    role     = data.get('role', 'candidate')

    if not email or not otp:
        return jsonify({'success': False, 'message': 'Email and OTP are required.'}), 400

    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        row = conn.execute(
            """SELECT id FROM password_reset_otps
               WHERE email=? AND otp=? AND used=0 AND expires_at > ?
               ORDER BY id DESC LIMIT 1""",
            (email, otp, now)
        ).fetchone()

    if not row:
        return jsonify({'success': False, 'message': 'Invalid or expired OTP. Please try again.'}), 400

    # Mark OTP consumed
    with get_db() as conn:
        conn.execute("UPDATE password_reset_otps SET used=1 WHERE id=?", (row['id'],))
        conn.commit()

    # Create the account now that email is verified
    result = register_user(name, email, password, role)
    if result.get('success'):
        session.clear()
        session['user_id'] = result['user']['id']
        
        # Send welcome email asynchronously-ish (fire and forget)
        try:
            import threading
            threading.Thread(target=_send_welcome_email, args=(email, name, role)).start()
        except:
            pass  # Non-blocking, don't fail registration if this errors

        return jsonify(result)
    else:
        return jsonify(result), 400


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """POST /api/auth/logout"""
    session.clear()  # Clear entire session, not just user_id
    return jsonify({'success': True})


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_me():
    """GET /api/auth/me"""
    user_id = session.get('user_id')
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if user:
            u_dict = dict(user)
            u_dict.pop('password', None)  # Never return password hash
            return jsonify({'success': True, 'user': u_dict})
    return jsonify({'success': False, 'message': 'User not found'}), 404


@auth_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """POST /api/auth/change_password → { current_password, new_password }"""
    user_id = session.get('user_id')

    data       = request.get_json(silent=True) or {}
    current_pw = data.get('current_password', '')
    new_pw     = data.get('new_password', '')

    if not current_pw or not new_pw:
        return jsonify({'success': False, 'message': 'Both passwords required'}), 400
    if len(new_pw) < 8:
        return jsonify({'success': False, 'message': 'New password must be at least 8 characters'}), 400
    if len(new_pw) > 128:
        return jsonify({'success': False, 'message': 'Password must not exceed 128 characters'}), 400

    from werkzeug.security import check_password_hash, generate_password_hash
    with get_db() as conn:
        user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        # Only hash-based comparison — no plaintext fallback
        try:
            is_valid = check_password_hash(user['password'], current_pw)
        except Exception:
            is_valid = False

        if not is_valid:
            return jsonify({'success': False, 'message': 'Current password is incorrect'}), 403

        conn.execute('UPDATE users SET password=? WHERE id=?',
                     (generate_password_hash(new_pw), user_id))
        conn.commit()

    # Invalidate session after password change — force re-login
    session.clear()
    return jsonify({'success': True, 'message': 'Password changed successfully! Please log in again.'})


@auth_bp.route('/landing_stats', methods=['GET'])
def landing_stats():
    """GET /api/auth/landing_stats — public stats for the landing page (no auth needed)."""
    with get_db() as conn:
        total_candidates = conn.execute("SELECT COUNT(*) FROM users WHERE role='candidate'").fetchone()[0]
        total_jobs       = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        total_apps       = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        avg_row          = conn.execute("SELECT AVG(ats_score) FROM users WHERE role='candidate' AND ats_score>0").fetchone()[0]
        avg_ats          = round(avg_row, 0) if avg_row else 0
    return jsonify({
        'resumes_analyzed': total_candidates,
        'jobs_matched':     total_jobs,
        'applications':     total_apps,
        'avg_ats':          int(avg_ats)
    })


# ── Forgot Password — Step 1: Send OTP ───────────────────────
@auth_bp.route('/forgot_password', methods=['POST'])
@limiter.limit("3 per minute")
def forgot_password():
    """
    POST /api/auth/forgot_password  →  { email }
    Generates a 6-digit OTP, stores it in DB, and emails it to the user.
    """
    data  = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'success': False, 'message': 'Email address is required.'}), 400

    with get_db() as conn:
        user = conn.execute("SELECT id, name FROM users WHERE email=?", (email,)).fetchone()

    if not user:
        # Return success-like response to prevent email enumeration
        return jsonify({
            'success': True,
            'message': 'If that email is registered, an OTP has been sent.'
        })

    otp        = _generate_otp()
    expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    user_name  = user['name']

    # Invalidate any existing OTPs for this email before inserting a new one
    with get_db() as conn:
        conn.execute("UPDATE password_reset_otps SET used=1 WHERE email=? AND used=0", (email,))
        conn.execute(
            "INSERT INTO password_reset_otps (email, otp, expires_at, used) VALUES (?,?,?,0)",
            (email, otp, expires_at)
        )
        conn.commit()

    sent = _send_otp_email(email, otp, user_name)

    if sent:
        return jsonify({
            'success': True,
            'message': f'OTP sent to {email}. Check your inbox (and spam folder).'
        })
    else:
        # Email not configured yet — return OTP in response for local dev
        return jsonify({
            'success': True,
            'dev_otp': otp,   # Only visible in dev; remove in production
            'message': (
                'Email service not configured. '
                'Add MAIL_SENDER and MAIL_APP_PASSWORD to your .env file. '
                f'Dev OTP: {otp}'
            )
        })


# ── Forgot Password — Step 2: Verify OTP ─────────────────────
@auth_bp.route('/verify_otp', methods=['POST'])
@limiter.limit("5 per minute")
def verify_otp():
    """
    POST /api/auth/verify_otp  →  { email, otp }
    Returns a short-lived reset_token stored in session on success.
    """
    data  = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    otp   = data.get('otp', '').strip()

    if not email or not otp:
        return jsonify({'success': False, 'message': 'Email and OTP are required.'}), 400

    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        row = conn.execute(
            """SELECT id FROM password_reset_otps
               WHERE email=? AND otp=? AND used=0 AND expires_at > ?
               ORDER BY id DESC LIMIT 1""",
            (email, otp, now)
        ).fetchone()

    if not row:
        return jsonify({'success': False, 'message': 'Invalid or expired OTP. Please try again.'}), 400

    # Mark OTP as used
    with get_db() as conn:
        conn.execute("UPDATE password_reset_otps SET used=1 WHERE id=?", (row['id'],))
        conn.commit()

    # Store verified email in session so reset_password can use it
    session['otp_verified_email'] = email
    return jsonify({'success': True, 'message': 'OTP verified! You can now set a new password.'})


# ── Forgot Password — Step 3: Reset Password ─────────────────
@auth_bp.route('/reset_password', methods=['POST'])
@limiter.limit("5 per minute")
def reset_password():
    """
    POST /api/auth/reset_password  →  { new_password }
    Requires a valid OTP session (set by /verify_otp).
    """
    verified_email = session.get('otp_verified_email')
    if not verified_email:
        return jsonify({'success': False, 'message': 'Session expired. Please restart the reset process.'}), 403

    data   = request.get_json(silent=True) or {}
    new_pw = data.get('new_password', '')

    if not new_pw:
        return jsonify({'success': False, 'message': 'New password is required.'}), 400
    if len(new_pw) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters.'}), 400

    from werkzeug.security import generate_password_hash
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET password=? WHERE email=?",
            (generate_password_hash(new_pw), verified_email)
        )
        conn.commit()

    # Clear the OTP session token
    session.pop('otp_verified_email', None)
    return jsonify({'success': True, 'message': 'Password reset successfully! Please log in with your new password.'})
