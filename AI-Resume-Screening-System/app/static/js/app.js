/* ============================================================
   HireAI — Main Application JavaScript
   Full SPA routing, charts, dynamic data, interactions
   ============================================================ */

'use strict';

// ── Company Domain Map → Clearbit Logo API ───────────────────
const COMPANY_DOMAINS = {
  // Indian IT Giants
  'tcs': 'tcs.com', 'tata consultancy services': 'tcs.com',
  'infosys': 'infosys.com',
  'wipro': 'wipro.com',
  'hcl': 'hcltech.com', 'hcl technologies': 'hcltech.com',
  'tech mahindra': 'techmahindra.com',
  'mphasis': 'mphasis.com',
  'hexaware': 'hexaware.com',
  'mindtree': 'mindtree.com',
  'ltimindtree': 'ltimindtree.com',
  'persistent systems': 'persistent.com',
  'coforge': 'coforge.com',
  'birlasoft': 'birlasoft.com',
  // Indian Product / Startup
  'flipkart': 'flipkart.com',
  'meesho': 'meesho.com',
  'zomato': 'zomato.com',
  'swiggy': 'swiggy.com',
  'ola': 'olacabs.com',
  'oyo': 'oyorooms.com',
  'razorpay': 'razorpay.com',
  'paytm': 'paytm.com',
  'phonepe': 'phonepe.com',
  'cred': 'cred.club',
  'nykaa': 'nykaa.com',
  'byju\'s': 'byjus.com', 'byjus': 'byjus.com',
  'unacademy': 'unacademy.com',
  'groww': 'groww.in',
  'zerodha': 'zerodha.com',
  'freshworks': 'freshworks.com',
  'zoho': 'zoho.com',
  'postman': 'postman.com',
  'browserstack': 'browserstack.com',
  'naukri.com': 'naukri.com', 'naukri': 'naukri.com',
  'nazara technologies': 'nazaratechnologies.com', 'nazara': 'nazaratechnologies.com',
  // Indian Telecom / Conglomerates
  'jio': 'jio.com', 'reliance jio': 'jio.com',
  'airtel': 'airtel.in',
  'bsnl': 'bsnl.co.in',
  'tata': 'tata.com',
  // Global Companies (India offices)
  'google': 'google.com',
  'microsoft': 'microsoft.com',
  'amazon': 'amazon.com', 'aws': 'aws.amazon.com',
  'meta': 'meta.com', 'facebook': 'meta.com',
  'apple': 'apple.com',
  'ibm': 'ibm.com',
  'oracle': 'oracle.com',
  'sap': 'sap.com', 'sap india': 'sap.com',
  'salesforce': 'salesforce.com', 'salesforce india': 'salesforce.com',
  'adobe': 'adobe.com',
  'accenture': 'accenture.com', 'accenture india': 'accenture.com',
  'deloitte': 'deloitte.com', 'deloitte india': 'deloitte.com',
  'pwc': 'pwc.com',
  'kpmg': 'kpmg.com',
  'ey': 'ey.com', 'ernst & young': 'ey.com',
  'mckinsey': 'mckinsey.com',
  'capgemini': 'capgemini.com',
  'cognizant': 'cognizant.com',
  'dxc': 'dxc.com', 'dxc technology': 'dxc.com',
  'atos': 'atos.net',
  'nvidia': 'nvidia.com',
  'intel': 'intel.com',
  'qualcomm': 'qualcomm.com',
  'samsung': 'samsung.com',
  'bosch': 'bosch.com',
  'siemens': 'siemens.com',
  'jp morgan': 'jpmorgan.com', 'jpmorgan': 'jpmorgan.com',
  'goldman sachs': 'goldmansachs.com',
  'morgan stanley': 'morganstanley.com',
  'deutsche bank': 'db.com',
  'hsbc': 'hsbc.com',
  'barclays': 'barclays.com',
  'linkedin': 'linkedin.com',
  'twitter': 'twitter.com', 'x': 'x.com',
  'uber': 'uber.com',
  'netflix': 'netflix.com',
  'spotify': 'spotify.com',
  'slack': 'slack.com',
  'atlassian': 'atlassian.com',
  'jfrog': 'jfrog.com',
  'gitlab': 'gitlab.com',
  'github': 'github.com',
  // ── Aerospace & Defence ──
  'isro': 'isro.gov.in',
  'hal': 'hal-india.co.in', 'hindustan aeronautics': 'hal-india.co.in',
  'drdo': 'drdo.gov.in',
  'safran': 'safran-group.com', 'safran engineering india': 'safran-group.com',
  'honeywell': 'honeywell.com', 'honeywell india': 'honeywell.com',
  // ── Electric Vehicles & CleanTech ──
  'ola electric': 'olaelectric.com',
  'tata motors': 'tatamotors.com', 'tata motors ev': 'tatamotors.com',
  'revolt motors': 'revoltmotors.in',
  'greaves electric': 'greavescotton.com',
  'renew power': 'renewpower.in',
  'ather energy': 'atherenergy.com',
  // ── Pharma & BioTech ──
  "dr. reddy's": 'drreddys.com', "dr. reddy's laboratories": 'drreddys.com',
  'sun pharma': 'sunpharma.com',
  'cipla': 'cipla.com',
  'medgenome': 'medgenome.com',
  // ── Government Tech ──
  'npci': 'npci.org.in', 'npci (upi)': 'npci.org.in',
  'uidai': 'uidai.gov.in', 'uidai (aadhaar)': 'uidai.gov.in',
  'nic': 'nic.in', 'nic (national informatics centre)': 'nic.in',
  'c-dac': 'cdac.in', 'c-dac india': 'cdac.in',
  // ── Retail & D2C ──
  'reliance retail': 'relianceretail.com',
  'decathlon': 'decathlon.co.in', 'decathlon india': 'decathlon.co.in',
  'mamaearth': 'mamaearth.in',
  'boat': 'boat-lifestyle.com', 'boat lifestyle': 'boat-lifestyle.com',
  // ── HR Tech ──
  'darwinbox': 'darwinbox.com',
  'hackerearth': 'hackerearth.com', 'iimjobs.com / hackerearth': 'hackerearth.com',
  'keka hr': 'keka.com', 'keka': 'keka.com',
  'spotdraft': 'spotdraft.com',
  // ── PropTech ──
  'nobroker': 'nobroker.in',
  '99acres': '99acres.com', '99acres (info edge)': '99acres.com',
  'square yards': 'squareyards.com',
  // ── AgriTech ──
  'dehaat': 'dehaat.com',
  'cropin': 'cropin.com', 'cropin technology': 'cropin.com',
  'agrostar': 'agrostar.in',
  // ── InsurTech ──
  'acko': 'acko.com', 'acko insurance': 'acko.com',
  'digit insurance': 'godigit.com', 'digit': 'godigit.com',
  'turtlemint': 'turtlemint.com',
  // ── Space Tech ──
  'skyroot': 'skyroot.in', 'skyroot aerospace': 'skyroot.in',
  'agnikul': 'agnikul.in', 'agnikul cosmos': 'agnikul.in',
  'pixxel': 'pixxel.space', 'pixxel space': 'pixxel.space',
  // ── Media & Content ──
  'zee5': 'zee5.com',
  'times internet': 'timesinternet.in',
  'dailyhunt': 'dailyhunt.in', 'verse innovation': 'dailyhunt.in',
  'inmobi': 'inmobi.com',
  // ── Supply Chain ──
  'juspay': 'juspay.in',
  'moglix': 'moglix.com',
  'ofbusiness': 'ofbusiness.com',
  // ── Automotive ──
  'mahindra tech': 'mahindra.com', 'mahindra': 'mahindra.com',
  'tata elxsi': 'tataelxsi.com',
  'maruti suzuki': 'marutisuzuki.com', 'maruti suzuki india': 'marutisuzuki.com',
  // ── International ──
  'uber': 'uber.com', 'uber india': 'uber.com',
  'linkedin': 'linkedin.com', 'linkedin india': 'linkedin.com',
  'adobe': 'adobe.com', 'adobe india': 'adobe.com',
  'spotify': 'spotify.com', 'spotify india': 'spotify.com',
  'netflix': 'netflix.com', 'netflix india': 'netflix.com',
  'zendesk': 'zendesk.com', 'zendesk india': 'zendesk.com',
  // ── More ──
  'polygon': 'polygon.technology', 'polygon (matic)': 'polygon.technology',
  'coindcx': 'coindcx.com',
  'dream11': 'dream11.com',
  'games24x7': 'games24x7.com',
  'mpl': 'mpl.live', 'mobile premier league': 'mpl.live',
  'hotstar': 'hotstar.com', 'jiostar': 'jiostar.com',
  'delhivery': 'delhivery.com',
  'bigbasket': 'bigbasket.com',
  'rapido': 'rapido.bike',
  'palo alto networks': 'paloaltonetworks.com',
  'nutanix': 'nutanix.com',
  'walmart': 'walmart.com', 'walmart global tech': 'walmart.com',
  'fractal analytics': 'fractal.ai', 'fractal': 'fractal.ai',
  'amd': 'amd.com', 'amd india': 'amd.com',
  'texas instruments': 'ti.com',
  'crowdstrike': 'crowdstrike.com',
  'tata communications': 'tatacommunications.com',
  'upstox': 'upstox.com',
  'pine labs': 'pinelabs.com',
  'bajaj finserv': 'bajajfinserv.in',
  'policybazaar': 'policybazaar.com',
  'chargebee': 'chargebee.com',
  'hasura': 'hasura.io',
  'druva': 'druva.com',
};

/**
 * Called when a Clearbit logo fails to load — replaces img with letter avatar.
 */
function onLogoError(img, abbr, color, textColor) {
  const div = document.createElement('div');
  div.style.cssText = `width:44px;height:44px;border-radius:8px;background:${color};color:${textColor};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;font-family:'Syne',sans-serif;`;
  div.textContent = abbr;
  img.parentNode.replaceChild(div, img);
}

/**
 * Returns HTML for a company logo — real Clearbit img with letter-avatar fallback.
 */
function getCompanyLogoHTML(companyName, color, textColor) {
  color     = color     || '#e0f2fe';
  textColor = textColor || '#0369a1';
  const key  = (companyName || '').toLowerCase().trim();
  const abbr = (companyName || '??').substring(0, 2).toUpperCase();
  const domain = COMPANY_DOMAINS[key]
    || Object.entries(COMPANY_DOMAINS).find(([k]) => key.includes(k))?.[1];

  if (domain) {
    // Use a named global function in onerror — avoids all escaping issues
    const c = encodeURIComponent(color);
    const t = encodeURIComponent(textColor);
    const a = encodeURIComponent(abbr);
    return `<img src="https://logo.clearbit.com/${domain}" alt="${abbr}"
      style="width:44px;height:44px;object-fit:contain;border-radius:6px;display:block;"
      onerror="onLogoError(this,'${abbr}','${color}','${textColor}')">`;
  }
  // No domain found — immediate letter avatar
  return `<div style="width:44px;height:44px;border-radius:8px;background:${color};color:${textColor};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;font-family:'Syne',sans-serif;">${abbr}</div>`;
}


// ── Data Store ──────────────────────────────────────────────
const DB = {
  currentUser: null,
  users: [],
  jobs: [],
  candidates: [],
  notifications: [],
  // Settings state
  settings: {
    emailNotif: true,
    smsNotif: false,
    jobAlerts: true,
    profileVisible: true,
    darkMode: false,
  }
};


// ── Router ───────────────────────────────────────────────────
const Router = {
  current: 'landing',
  innerPages: { cand: 'dash', admin: 'dash' },

  // Pages that should be saved to the URL hash (dashboard pages)
  // ALL pages & sections that should persist in the URL hash on refresh
  _hashPages: new Set([
    // Top-level guest pages
    'landing', 'login', 'register', 'forgot',
    'about', 'blog', 'careers', 'press', 'contact', 'legal', 'product',
    // Portal root pages
    'cand', 'admin',
  ]),

  go(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const el = document.getElementById('page-' + page);
    if (el) { el.classList.add('active'); window.scrollTo(0,0); }
    this.current = page;
    // Clear login fields when navigating to login page (prevent stale autofill)
    if (page === 'login') {
      const emailEl = document.getElementById('login-email');
      const passEl  = document.getElementById('login-password');
      if (emailEl) emailEl.value = '';
      if (passEl)  passEl.value  = '';
    }
    // Clear register fields when navigating to register page
    if (page === 'register') {
      ['reg-fname','reg-lname','reg-email','reg-pass','reg-cpass'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
      });
    }
    // Save page to URL hash so refresh restores it
    if (this._hashPages.has(page)) {
      history.replaceState(null, '', '#' + page);
    }
  },

  inner(portal, section) {
    document.querySelectorAll(`[data-portal="${portal}"]`).forEach(s => s.classList.add('hidden'));
    const el = document.getElementById(`${portal}-${section}`);
    if (el) el.classList.remove('hidden');
    this.innerPages[portal] = section;
    // Also update the hash to include the inner section
    history.replaceState(null, '', '#' + portal + '-' + section);
  },

  // Like inner() but does NOT touch the URL hash — used during portal init
  // so the original page hash is preserved for refresh restoration.
  _silentInner(portal, section) {
    document.querySelectorAll(`[data-portal="${portal}"]`).forEach(s => s.classList.add('hidden'));
    const el = document.getElementById(`${portal}-${section}`);
    if (el) el.classList.remove('hidden');
    this.innerPages[portal] = section;
  }
};

// ── Auth ─────────────────────────────────────────────────────
const Auth = {
  selectedRole: { login: 'candidate', register: 'candidate' },

  login(form) {
    const email    = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    const role     = this.selectedRole.login;

    if (!email || !password) { Toast.show('Please fill in all fields.', 'warning'); return; }
    
    fetch('/api/auth/login', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, password, role})
    }).then(r=>r.json()).then(data => {
        if(!data.success) { Toast.show(data.message || 'Invalid credentials.', 'error'); return; }
        const user = data.user;
        user.avatar = user.name.slice(0,2).toUpperCase();
        DB.currentUser = user;
        this.setupPortal(user);
        Router.go(user.role === 'hr' ? 'admin' : 'cand');
        Toast.show(`Welcome back, ${user.name.split(' ')[0]}! <i class="fa-solid fa-hand-sparkles" style="color: #34d399; margin-left: 4px;"></i>`, 'success');

        fetchJobsFromServer();
        fetchNotificationsFromServer(user.id);
        if(user.role === 'hr') {
            fetchCandidatesFromServer();
            fetchAdminStats();
        } else {
            fetchCandidateStats(user.id);
            fetchCandidateProfile(user.id);
        }
    }).catch(e => Toast.show('Server error', 'error'));
  },

  // ── Step 1: Validate form → Send OTP to email ─────────────
  sendRegisterOtp(isResend = false) {
    const fname = document.getElementById('reg-fname').value.trim();
    const lname = document.getElementById('reg-lname').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const pass  = document.getElementById('reg-pass').value;
    const cpass = document.getElementById('reg-cpass').value;

    const errorEl  = document.getElementById('reg-step1-error');
    const errorMsg = document.getElementById('reg-step1-error-msg');
    errorEl.classList.add('hidden');

    if (!fname || !lname) { errorMsg.textContent = 'Please enter your first and last name.'; errorEl.classList.remove('hidden'); return; }
    if (!email) { errorMsg.textContent = 'Please enter a valid email address.'; errorEl.classList.remove('hidden'); return; }
    if (!pass)  { errorMsg.textContent = 'Please enter a password.'; errorEl.classList.remove('hidden'); return; }
    if (pass.length < 6) { errorMsg.textContent = 'Password must be at least 6 characters.'; errorEl.classList.remove('hidden'); return; }
    if (pass !== cpass) { errorMsg.textContent = 'Passwords do not match.'; errorEl.classList.remove('hidden'); return; }

    const btn = document.getElementById('reg-send-otp-btn');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending OTP...'; }

    fetch('/api/auth/send_register_otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, name: `${fname} ${lname}` })
    }).then(r => r.json()).then(data => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-envelope" style="margin-right:8px;"></i> Verify Email & Continue'; }
      if (data.success) {
        // Switch to Step 2
        document.getElementById('reg-step-1').classList.add('hidden');
        document.getElementById('reg-step-2').classList.remove('hidden');
        document.getElementById('reg-otp').value = '';
        document.getElementById('reg-otp-error').classList.add('hidden');

        const hint = document.getElementById('reg-otp-hint');
        if (hint) hint.textContent = `OTP sent to ${email}. Check your inbox (and spam folder).`;
        const display = document.getElementById('reg-otp-email-display');
        if (display) display.textContent = `OTP sent to ${email}`;

        if (data.dev_otp) {
          document.getElementById('reg-otp').value = data.dev_otp;
          Toast.show(`Dev mode: OTP auto-filled → ${data.dev_otp}`, 'warning', 8000);
        } else {
          Toast.show(isResend ? 'New OTP sent! Check your inbox.' : `Verification OTP sent to ${email}!`, 'success');
        }
        setTimeout(() => document.getElementById('reg-otp').focus(), 100);
      } else {
        errorMsg.textContent = data.message || 'Failed to send OTP.';
        errorEl.classList.remove('hidden');
        Toast.show(data.message || 'Error sending OTP.', 'error');
      }
    }).catch(() => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-envelope" style="margin-right:8px;"></i> Verify Email & Continue'; }
      Toast.show('Server error — please try again.', 'error');
    });
  },

  // ── Step 2: Verify OTP → Create Account ───────────────────
  verifyRegisterOtp() {
    const otp    = document.getElementById('reg-otp').value.trim();
    const email  = document.getElementById('reg-email').value.trim();
    const fname  = document.getElementById('reg-fname').value.trim();
    const lname  = document.getElementById('reg-lname').value.trim();
    const pass   = document.getElementById('reg-pass').value;
    const role   = this.selectedRole.register;

    const btn      = document.getElementById('reg-verify-btn');
    const errorEl  = document.getElementById('reg-otp-error');
    const errorMsg = document.getElementById('reg-otp-error-msg');

    errorEl.classList.add('hidden');

    if (!otp || otp.length !== 6) { Toast.show('Please enter the 6-digit OTP.', 'warning'); return; }

    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying & Creating Account...'; }

    fetch('/api/auth/verify_register_otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, otp, name: `${fname} ${lname}`, password: pass, role })
    }).then(r => r.json()).then(data => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-check-circle" style="margin-right:8px;"></i> Verify & Create Account'; }
      if (!data.success) {
        errorMsg.textContent = data.message || 'Invalid or expired OTP.';
        errorEl.classList.remove('hidden');
        Toast.show(data.message || 'OTP verification failed.', 'error');
        return;
      }
      // Account created!
      const user = data.user;
      user.avatar = user.name.slice(0, 2).toUpperCase();
      DB.currentUser = user;
      this.setupPortal(user);
      Router.go(user.role === 'hr' ? 'admin' : 'cand');
      Toast.show(`Account created! Welcome, ${fname}! <i class="fa-solid fa-wand-magic-sparkles"></i>`, 'success');

      // Reset register form for next use
      ['reg-fname','reg-lname','reg-email','reg-pass','reg-cpass','reg-otp'].forEach(id => {
        const el = document.getElementById(id); if (el) el.value = '';
      });
      document.getElementById('reg-step-2').classList.add('hidden');
      document.getElementById('reg-step-1').classList.remove('hidden');

      fetchJobsFromServer();
      fetchNotificationsFromServer(user.id);
      if (user.role === 'hr') {
        fetchCandidatesFromServer();
        fetchAdminStats();
      } else {
        fetchCandidateStats(user.id);
        fetchCandidateProfile(user.id);
      }
    }).catch(() => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-check-circle" style="margin-right:8px;"></i> Verify & Create Account'; }
      Toast.show('Server error — please try again.', 'error');
    });
  },

  // Legacy register() kept as alias in case called elsewhere
  register() { this.sendRegisterOtp(); },


  // ── Step 1: Send OTP ───────────────────────────────────────
  forgotPwd(isResend = false) {
    const email = document.getElementById('forgot-email').value.trim();
    if (!email) { Toast.show('Please enter your email address.', 'warning'); return; }

    const btn      = document.getElementById('forgot-send-btn');
    const errorEl  = document.getElementById('forgot-error');
    const errorMsg = document.getElementById('forgot-error-msg');

    errorEl.classList.add('hidden');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending OTP...'; }

    fetch('/api/auth/forgot_password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    }).then(r => r.json()).then(data => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-paper-plane" style="margin-right:8px;"></i> Send OTP'; }
      if (data.success) {
        // Switch to Step 2
        document.getElementById('forgot-step-1').classList.add('hidden');
        document.getElementById('forgot-step-2').classList.remove('hidden');
        document.getElementById('forgot-otp').value = '';
        document.getElementById('forgot-otp-error').classList.add('hidden');

        const hint = document.getElementById('forgot-otp-hint');
        if (hint) hint.textContent = `OTP sent to ${email}. Check your inbox (and spam folder).`;

        // Dev mode: auto-fill OTP if server returned it (email not configured)
        if (data.dev_otp) {
          document.getElementById('forgot-otp').value = data.dev_otp;
          Toast.show(`Dev mode: OTP auto-filled → ${data.dev_otp}`, 'warning', 8000);
        } else {
          Toast.show(isResend ? 'New OTP sent! Check your inbox.' : `OTP sent to ${email}!`, 'success');
        }
        setTimeout(() => document.getElementById('forgot-otp').focus(), 100);
      } else {
        if (errorMsg) errorMsg.textContent = data.message || 'Email not found in our system.';
        errorEl.classList.remove('hidden');
        Toast.show(data.message || 'Email not found.', 'error');
      }
    }).catch(() => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-paper-plane" style="margin-right:8px;"></i> Send OTP'; }
      Toast.show('Server error — please try again.', 'error');
    });
  },

  // ── Step 2: Verify OTP ─────────────────────────────────────
  verifyOtp() {
    const email    = document.getElementById('forgot-email').value.trim();
    const otp      = document.getElementById('forgot-otp').value.trim();
    const btn      = document.getElementById('forgot-verify-btn');
    const errorEl  = document.getElementById('forgot-otp-error');
    const errorMsg = document.getElementById('forgot-otp-error-msg');

    if (!otp || otp.length !== 6) {
      Toast.show('Please enter the 6-digit OTP.', 'warning'); return;
    }

    errorEl.classList.add('hidden');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...'; }

    fetch('/api/auth/verify_otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, otp })
    }).then(r => r.json()).then(data => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-check-circle" style="margin-right:8px;"></i> Verify OTP'; }
      if (data.success) {
        // Switch to Step 3
        document.getElementById('forgot-step-2').classList.add('hidden');
        document.getElementById('forgot-step-3').classList.remove('hidden');
        document.getElementById('forgot-new-pass').value = '';
        document.getElementById('forgot-conf-pass').value = '';
        document.getElementById('forgot-reset-error').classList.add('hidden');
        Toast.show('OTP verified! Set your new password.', 'success');
        setTimeout(() => document.getElementById('forgot-new-pass').focus(), 100);
      } else {
        if (errorMsg) errorMsg.textContent = data.message || 'Invalid or expired OTP.';
        errorEl.classList.remove('hidden');
        Toast.show(data.message || 'Invalid OTP.', 'error');
      }
    }).catch(() => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-check-circle" style="margin-right:8px;"></i> Verify OTP'; }
      Toast.show('Server error — please try again.', 'error');
    });
  },

  // ── Step 3: Reset Password ─────────────────────────────────
  resetPassword() {
    const newPw   = document.getElementById('forgot-new-pass').value;
    const confPw  = document.getElementById('forgot-conf-pass').value;
    const btn     = document.getElementById('forgot-reset-btn');
    const errorEl = document.getElementById('forgot-reset-error');
    const errMsg  = document.getElementById('forgot-reset-error-msg');

    errorEl.classList.add('hidden');

    if (!newPw) { Toast.show('Please enter a new password.', 'warning'); return; }
    if (newPw.length < 8) {
      errMsg.textContent = 'Password must be at least 8 characters.';
      errorEl.classList.remove('hidden'); return;
    }
    if (newPw !== confPw) {
      errMsg.textContent = 'Passwords do not match.';
      errorEl.classList.remove('hidden'); return;
    }

    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Resetting...'; }

    fetch('/api/auth/reset_password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_password: newPw })
    }).then(r => r.json()).then(data => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-shield-halved" style="margin-right:8px;"></i> Reset Password'; }
      if (data.success) {
        Toast.show('Password reset! Please log in with your new password.', 'success', 5000);
        // Reset all steps & navigate to login
        setTimeout(() => {
          document.getElementById('forgot-step-3').classList.add('hidden');
          document.getElementById('forgot-step-1').classList.remove('hidden');
          document.getElementById('forgot-email').value = '';
          document.getElementById('forgot-otp').value = '';
          document.getElementById('forgot-new-pass').value = '';
          document.getElementById('forgot-conf-pass').value = '';
          Router.go('login');
        }, 1500);
      } else {
        errMsg.textContent = data.message || 'Failed to reset password. Please start over.';
        errorEl.classList.remove('hidden');
        Toast.show(data.message || 'Reset failed.', 'error');
      }
    }).catch(() => {
      if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-shield-halved" style="margin-right:8px;"></i> Reset Password'; }
      Toast.show('Server error — please try again.', 'error');
    });
  },


  logout() {
    fetch('/api/auth/logout', { method: 'POST' }).then(() => {
      DB.currentUser = null;
      Router.go('landing');
      Toast.show('Logged out successfully! <i class="fa-solid fa-right-from-bracket" style="color: #34d399; margin-left: 4px;"></i>', 'success');
      setTimeout(() => window.location.reload(), 1000);
    });
  },

  setupPortal(user) {
    const avatar = user.avatar || user.name.slice(0,2).toUpperCase();
    const isHR   = user.role === 'hr';

    // --- Sidebar + topbar names/avatars ---
    document.querySelectorAll('.cand-name').forEach(el => el.textContent = user.name);
    document.querySelectorAll('.cand-role').forEach(el => el.textContent = isHR ? 'HR Admin' : 'Candidate');
    document.querySelectorAll('.admin-name').forEach(el => el.textContent = user.name);

    // Apply avatar — use saved photo if available, else initials
    const candPhoto  = localStorage.getItem('hireai_cand_photo');
    const adminPhoto = localStorage.getItem('hireai_admin_photo');
    document.querySelectorAll('.cand-avatar').forEach(el => {
      if (candPhoto) {
        el.textContent = '';
        el.style.backgroundImage    = `url('${candPhoto}')`;
        el.style.backgroundSize     = 'cover';
        el.style.backgroundPosition = 'center';
        el.style.color              = 'transparent';
      } else {
        el.textContent = avatar;
        el.style.backgroundImage = '';
        el.style.color = '';
      }
    });
    document.querySelectorAll('.admin-avatar').forEach(el => {
      if (adminPhoto) {
        el.textContent = '';
        el.style.backgroundImage    = `url('${adminPhoto}')`;
        el.style.backgroundSize     = 'cover';
        el.style.backgroundPosition = 'center';
        el.style.color              = 'transparent';
      } else {
        el.textContent = avatar;
        el.style.backgroundImage = '';
        el.style.color = '';
      }
    });

    // --- Populate candidate profile form with REAL user data ---
    const setVal = (id, v) => { const el = document.getElementById(id); if(el) el.value = v || ''; };
    setVal('cand-profile-name',  user.name ? user.name.split(' ')[0] : '');
    setVal('cand-profile-lname', user.name ? (user.name.split(' ')[1] || '') : '');
    setVal('cand-profile-email', user.email || '');
    setVal('cand-profile-phone', user.phone || '');
    setVal('cand-profile-loc', user.location || '');
    setVal('cand-profile-link', user.linkedin || '');
    setVal('cand-profile-git', user.github || '');
    setVal('cand-profile-sum', user.summary || '');
    setVal('cand-profile-edu', user.education || '');

    // --- ML Insights card (real data from DB) ---
    const clusterLabel  = user.cluster_label || 'Unclustered';
    const isOutlier     = user.is_outlier === 1 || user.is_outlier === true;
    const atsScore      = user.ats_score || 0;

    // Cluster label
    const clEl = document.getElementById('profile-cluster-label');
    if (clEl) clEl.textContent = clusterLabel;

    // Cluster badge in header
    const clBadge = document.getElementById('profile-cluster-badge');
    if (clBadge) { clBadge.textContent = clusterLabel; clBadge.style.display = ''; }

    // Outlier status
    const outlierEl   = document.getElementById('profile-outlier-status');
    const outlierIcon = document.getElementById('profile-outlier-icon');
    const outlierBadge = document.getElementById('profile-outlier-badge');
    if (outlierEl) {
      if (isOutlier) {
        outlierEl.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Suspicious Flag Active';
        outlierEl.style.color = '#dc2626';
        if (outlierIcon) { outlierIcon.innerHTML = '<i class="fa-solid fa-triangle-exclamation" style="color: #dc2626;"></i>'; outlierIcon.style.background = 'rgba(220,38,38,.12)'; }
        if (outlierBadge) outlierBadge.style.display = '';
      } else {
        outlierEl.innerHTML = '<i class="fa-solid fa-check"></i> Normal Profile';
        outlierEl.style.color = '#16a34a';
        if (outlierIcon) { outlierIcon.innerHTML = '<i class="fa-solid fa-shield-halved" style="color: #16a34a;"></i>'; outlierIcon.style.background = 'rgba(22,163,74,.12)'; }
      }
    }

    // Profile Strength: based on fields filled in
    const filledFields = [user.phone, user.location, user.linkedin, user.github, user.summary, user.education, user.skills].filter(Boolean).length;
    const strengthPct  = Math.round((filledFields / 7) * 100);
    const strengthEl   = document.getElementById('profile-strength-label');
    if (strengthEl) {
      const label = strengthPct >= 80 ? '🟢 Strong' : strengthPct >= 50 ? '🟡 Medium' : '🔴 Needs Work';
      strengthEl.textContent = `${label} (${strengthPct}%)`;
      strengthEl.style.color = strengthPct >= 80 ? '#16a34a' : strengthPct >= 50 ? '#d97706' : '#dc2626';
    }

    setVal('admin-profile-name', user.name || '');
    setVal('admin-profile-email', user.email || '');
    setVal('admin-profile-phone', user.phone || '');
    setVal('admin-profile-loc', user.location || '');

    // --- Candidate welcome banner with real name ---
    const banner = document.getElementById('cand-welcome-name');
    if(banner) banner.textContent = user.name.split(' ')[0];

    // --- New user: show upload CTA, hide stats until resume uploaded ---
    const hasResume = user.ats_score && user.ats_score > 0;
    const newUserBanner = document.getElementById('new-user-banner');
    const resumePrompt  = document.getElementById('resume-upload-prompt');
    if(newUserBanner) newUserBanner.classList.toggle('hidden', hasResume);
    if(resumePrompt)  resumePrompt.classList.toggle('hidden', hasResume);

    // --- Init inner pages (use _silentInner to avoid overwriting the URL hash) ---
    Router._silentInner('cand', 'dash');
    Router._silentInner('admin', 'dash');
  },

  setRole(portal, role, el) {
    this.selectedRole[portal] = role;
    el.closest('.role-picker').querySelectorAll('.role-option').forEach(o => o.classList.remove('active'));
    el.classList.add('active');
  },

  checkSession() {
    // ── CRITICAL: capture the hash NOW, before anything can overwrite it ──
    const savedHash = window.location.hash.replace('#', '');

    fetch('/api/auth/me')
      .then(r => r.json())
      .then(data => {
        if (data.success && data.user) {
          const user = data.user;
          user.avatar = user.name.slice(0,2).toUpperCase();
          DB.currentUser = user;
          // setupPortal uses _silentInner internally so it won't touch the hash
          this.setupPortal(user);

          // ── Restore the page from the hash captured at startup ──
          const portalPage = user.role === 'hr' ? 'admin' : 'cand';

          if (savedHash && savedHash.startsWith(portalPage)) {
            // e.g. savedHash = 'admin-jobs' → go to portal, then switch inner section
            const parts = savedHash.split('-');
            Router.go(portalPage);
            if (parts.length >= 2) {
              const section = parts.slice(1).join('-'); // handle multi-word like 'job-rankings'
              const sectionEl = document.getElementById(`${portalPage}-${section}`);
              if (sectionEl) {
                Router.inner(portalPage, section);
              } else {
                // section element not found, stay on default dash
                Router.inner(portalPage, 'dash');
              }
            } else {
              // hash was just 'admin' or 'cand' with no section
              Router.inner(portalPage, 'dash');
            }
          } else {
            // No valid portal hash — go to default dashboard
            Router.go(portalPage);
            Router.inner(portalPage, 'dash');
          }

          fetchJobsFromServer();
          fetchNotificationsFromServer(user.id);
          if (user.role === 'hr') {
              fetchCandidatesFromServer();
              fetchAdminStats();
          } else {
              fetchCandidateStats(user.id);
              fetchCandidateProfile(user.id);
          }
        } else {
          // ── Not logged in: restore guest page from hash if present ──
          const GUEST_PAGES = new Set([
            'landing', 'login', 'register', 'forgot',
            'about', 'blog', 'careers', 'press', 'contact', 'legal', 'product',
          ]);
          if (savedHash && GUEST_PAGES.has(savedHash)) {
            Router.go(savedHash);
          }
          // If no valid hash, page stays as default (landing) which is already shown by CSS
        }
      })
      .catch(e => console.error('Session check failed', e));
  }
};

// Check session on page load
document.addEventListener('DOMContentLoaded', () => {
  // ── Restore guest-accessible pages from URL hash BEFORE session check ──
  // Pages that don't require authentication can be restored immediately.
  const GUEST_PAGES = new Set([
    'landing', 'login', 'register', 'forgot',
    'about', 'blog', 'careers', 'press', 'contact', 'legal', 'product',
  ]);
  const hashOnLoad = window.location.hash.replace('#', '');
  if (hashOnLoad && GUEST_PAGES.has(hashOnLoad)) {
    Router.go(hashOnLoad);
  }
  // Session check will override with the correct portal page if user is logged in
  Auth.checkSession();
});

// ── Toast ─────────────────────────────────────────────────────
const Toast = {
  show(msg, type='info', duration=4000) {
    const icons = { success:'fa-check-circle', error:'fa-times-circle', warning:'fa-exclamation-triangle', info:'fa-info-circle' };
    const c = document.getElementById('toast-container');
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `<i class="fas ${icons[type]}"></i><span>${msg}</span><span class="toast-close" onclick="this.parentElement.remove()">✕</span>`;
    c.appendChild(t);
    setTimeout(() => t.style.animation='slideInRight .3s ease reverse', duration - 400);
    setTimeout(() => t.remove(), duration);
  }
};

// ── Sidebar ───────────────────────────────────────────────────
const Sidebar = {
  open(portal) {
    document.getElementById(`sb-${portal}`).classList.add('open');
    document.getElementById(`mob-overlay-${portal}`).classList.add('show');
  },
  close(portal) {
    document.getElementById(`sb-${portal}`).classList.remove('open');
    document.getElementById(`mob-overlay-${portal}`).classList.remove('show');
  },
  setActive(el) {
    el.closest('.sb-nav').querySelectorAll('.sb-item').forEach(i => i.classList.remove('active'));
    el.classList.add('active');
  }
};

// ── Modal ─────────────────────────────────────────────────────
const Modal = {
  open(id) { document.getElementById(id).classList.add('show'); },
  close(id) { document.getElementById(id).classList.remove('show'); },
  closeAll() { document.querySelectorAll('.modal-backdrop.show').forEach(m => m.classList.remove('show')); }
};

// ── Tabs ──────────────────────────────────────────────────────
function switchTab(el, group) {
  document.querySelectorAll(`[data-tabgroup="${group}"]`).forEach(t => t.classList.remove('active'));
  el.classList.add('active');
}

// ── Candidate Status Update ───────────────────────────────────
function updateCandidateStatus(id, status) {
  fetch('/api/admin/update_status', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({app_id: id, status: status})
  }).then(r=>r.json()).then(data => {
      if(data.success) {
          const candidate = DB.candidates.find(c => c.id === parseInt(id));
          if (candidate) {
            candidate.status = status;
            UI.renderCandidatesTable();
            Toast.show(`${candidate.name} status updated to ${status}.`, 'success');
            // Refresh tab counts live
            setEl('tab-count-all',         DB.candidates.length);
            setEl('tab-count-shortlisted', DB.candidates.filter(c=>c.status==='Shortlisted').length);
            setEl('tab-count-reviewing',   DB.candidates.filter(c=>c.status==='Reviewing'||c.status==='Pending').length);
            setEl('tab-count-rejected',    DB.candidates.filter(c=>c.status==='Rejected').length);
          }
      }
  });
}

// ── UI Renderers ──────────────────────────────────────────────
const UI = {
  renderJobCards(containerId, jobs, isCandidateView = true, page = 0) {
    const c = document.getElementById(containerId);
    if (!c) return;

    const PAGE_SIZE = 12;
    const start   = page * PAGE_SIZE;
    const slice   = jobs.slice(start, start + PAGE_SIZE);
    const hasMore = start + PAGE_SIZE < jobs.length;

    if (page === 0) c.innerHTML = '';

    const temp = document.createElement('div');
    temp.innerHTML = slice.map(j => {
      const key    = (j.company || '').toLowerCase().trim();
      const domain = COMPANY_DOMAINS[key]
        || Object.entries(COMPANY_DOMAINS).find(([k]) => key.includes(k))?.[1];
      const abbr   = (j.company || '??').substring(0, 2).toUpperCase();
      const color  = j.color    || '#e0f2fe';
      const tcolor = j.textColor || '#1e40af';

      // Google Favicon — fast, reliable, no Clearbit delay
      const logoHTML = domain
        ? `<img
            src="https://www.google.com/s2/favicons?domain=${domain}&sz=128"
            loading="eager"
            alt="${abbr}"
            width="40" height="40"
            style="object-fit:contain;border-radius:6px;display:block;"
           >`
        : `<div style="width:44px;height:44px;border-radius:8px;background:${color};color:${tcolor};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;font-family:'Syne',sans-serif;">${abbr}</div>`;

      return `
      <div class="job-card ${j.match >= 85 ? 'featured' : ''}">
        ${j.match >= 85 ? `<div class="job-card-badge"><span class="badge badge-teal">⭐ Top Match</span></div>` : ''}
        <div class="company-row">
          <div class="company-logo" style="background:#fff;">${logoHTML}</div>
          <div>
            <div class="job-title">${j.title}</div>
            <div class="company-name">${j.company}</div>
          </div>
        </div>
        <div class="job-metas">
          <div class="job-meta"><i class="fas fa-map-marker-alt"></i> ${j.location}</div>
          <div class="job-meta"><i class="fas fa-clock"></i> ${j.type}</div>
          <div class="job-meta"><i class="fas fa-rupee-sign"></i> ${j.salary}</div>
        </div>
        <div class="job-skills">
          ${j.skills.slice(0,3).map(s => `<span class="job-skill-tag">${s}</span>`).join('')}
        </div>
        ${isCandidateView ? `
        <div class="match-row">
          <div class="match-labels"><span>AI Match Score</span><strong>${j.match}%</strong></div>
          <div class="progress"><div class="progress-bar" style="width:${j.match}%;background:linear-gradient(90deg,#00c9a7,#1260cc)"></div></div>
        </div>
        <button class="btn btn-primary btn-full mt-2" onclick="applyJob(${j.id})">Apply Now</button>
        ` : `
        <div style="display:flex;gap:8px;margin-top:14px;padding-top:14px;border-top:1px solid var(--border)">
          <button class="btn btn-navy" style="flex:1;font-size:13px" onclick="viewJobRankings(${j.id})">View Rankings</button>
          <button class="btn btn-outline btn-sm" onclick="editJob(${j.id})"><i class="fas fa-edit"></i></button>
          <button class="btn btn-outline btn-sm" onclick="deleteJob(${j.id})"><i class="fas fa-trash"></i></button>
        </div>
        <div style="margin-top:10px;font-size:12px;color:var(--text-3)"><i class="fas fa-users"></i> ${j.applicants} applicants · <span class="badge ${j.status==='Active'?'badge-success':'badge-warning'}" style="font-size:11px">${j.status}</span></div>
        `}
      </div>
    `}).join('');

    // Move children as direct grid elements (DocumentFragment preserves CSS grid)
    const frag = document.createDocumentFragment();
    while (temp.firstChild) frag.appendChild(temp.firstChild);
    c.appendChild(frag);

    // Load-More button
    const oldBtn = document.getElementById(`${containerId}-load-more`);
    if (oldBtn) oldBtn.remove();
    if (hasMore) {
      const btn = document.createElement('button');
      btn.id = `${containerId}-load-more`;
      btn.className = 'btn btn-outline';
      btn.style.cssText = 'width:100%;margin-top:20px;padding:14px;font-size:14px;';
      btn.innerHTML = `<i class="fas fa-chevron-down"></i> Load More (${jobs.length - start - PAGE_SIZE} remaining)`;
      btn.onclick = () => { btn.remove(); this.renderJobCards(containerId, jobs, isCandidateView, page + 1); };
      c.parentNode.insertBefore(btn, c.nextSibling);
    }
  },


  renderCandidatesTable(filter='All') {
    const tbody = document.getElementById('candidates-tbody');
    if (!tbody) return;
    let data = DB.candidates;
    if (filter === 'Flagged')  data = data.filter(c => c.outlier_flag);
    else if (filter !== 'All') data = data.filter(c => c.status === filter);

    tbody.innerHTML = data.map((c,i) => `
      <tr style="${c.outlier_flag ? 'background:rgba(220,38,38,0.04);border-left:3px solid #dc2626' : ''}">
        <td>${this.rankBadge(i+1)}</td>
        <td>
          <div style="display:flex;align-items:center;gap:10px">
            <div class="avatar avatar-sm" style="background:${this.avatarColor(c.name)};color:#fff">${c.name.slice(0,2).toUpperCase()}</div>
            <div>
              <div class="fw-600">${c.name}</div>
              <div class="text-xs text-muted">${c.email}</div>
              ${c.outlier_flag ? `<span title="${c.outlier_reason}" style="display:inline-flex;align-items:center;gap:3px;margin-top:3px;background:#fee2e2;color:#dc2626;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;border:1px solid #fca5a5">⚠️ SUSPICIOUS</span>` : ''}
              <span style="display:inline-block;margin-top:3px;background:#eff6ff;color:#2563eb;font-size:10px;padding:2px 6px;border-radius:4px;font-weight:600">${c.cluster_label}</span>
            </div>
          </div>
        </td>
        <td><span class="text-sm">${c.degree}</span></td>
        <td>${c.job}</td>
        <td>
          <div style="display:flex;gap:4px;flex-wrap:wrap;max-width:220px">
            ${c.skills.slice(0, 4).map(s=>`<span class="badge badge-primary" style="font-size:11px">${s}</span>`).join('')}
            ${c.skills.length > 4 ? `<span class="badge badge-gray" style="font-size:11px">+${c.skills.length - 4} more</span>` : ''}
          </div>
        </td>
        <td><span class="badge ${this.atsBadge(c.ats)}">${c.ats}/100</span></td>
        <td><strong style="color:${c.match>=80?'#16a34a':c.match>=60?'#d97706':'#dc2626'}">${c.match}%</strong></td>
        <td>${this.statusBadge(c.status)}</td>
        <td>
          <div style="display:flex;gap:6px">
            <button class="btn btn-sm btn-primary" onclick="viewCandidate(${c.id})">View</button>
            <select class="form-control" style="padding:5px 8px;font-size:12px;height:auto;width:auto" onchange="updateCandidateStatus(${c.id},this.value)">
              <option ${c.status==='Reviewing'?'selected':''}>Reviewing</option>
              <option ${c.status==='Shortlisted'?'selected':''}>Shortlisted</option>
              <option ${c.status==='Pending'?'selected':''}>Pending</option>
              <option ${c.status==='Rejected'?'selected':''}>Rejected</option>
            </select>
          </div>
        </td>
      </tr>
    `).join('') || `<tr><td colspan="9" style="text-align:center;padding:30px;color:var(--text-3)">No candidates found</td></tr>`;
  },

  renderRankingsTable(jobId) {
    const tbody = document.getElementById('rankings-tbody');
    if (!tbody) return;
    const data = [...DB.candidates].sort((a,b) => b.ats - a.ats);
    tbody.innerHTML = data.map((c,i) => `
      <tr ${i===0?'class="top-rank-row"':''}>
        <td>${this.rankBadge(i+1)}</td>
        <td>
          <div style="display:flex;align-items:center;gap:10px">
            <div class="avatar avatar-sm" style="background:${this.avatarColor(c.name)};color:#fff">${c.name.slice(0,2).toUpperCase()}</div>
            <div class="fw-600">${c.name}</div>
          </div>
        </td>
        <td>${c.job}</td>
        <td><span class="badge ${this.atsBadge(c.ats)}">${c.ats}/100</span></td>
        <td><strong>${c.match}%</strong></td>
        <td>${c.exp}</td>
        <td>${c.sim.toFixed(2)}</td>
        <td><strong style="font-size:16px;font-family:'Syne',sans-serif">${Math.round((c.ats*0.4 + c.match*0.3 + c.sim*100*0.3))}</strong></td>
        <td>
          ${i===0?`<button class="btn btn-success btn-sm" onclick="updateCandidateStatus(${c.id},'Shortlisted');Toast.show('${c.name} shortlisted!','success')">✓ Hire</button>`
          :i>=data.length-2?`<button class="btn btn-danger btn-sm" onclick="updateCandidateStatus(${c.id},'Rejected');Toast.show('${c.name} rejected.','info')">Reject</button>`
          :`<button class="btn btn-warning btn-sm" onclick="updateCandidateStatus(${c.id},'Shortlisted');Toast.show('${c.name} shortlisted!','success')">Shortlist</button>`}
        </td>
      </tr>
    `).join('');
  },

  renderNotifications(portal) {
    const c = document.getElementById(`${portal}-notif-list`);
    if (!c) return;
    
    if (!DB.notifications || DB.notifications.length === 0) {
      c.innerHTML = `<div style="padding:40px 20px;text-align:center;color:var(--text-3);font-size:14px;">
        <i class="fas fa-bell-slash" style="font-size:32px;opacity:0.3;margin-bottom:12px;display:block"></i>
        You're all caught up! No notifications yet.
      </div>`;
      return;
    }

    c.innerHTML = DB.notifications.map(n => `
      <div class="notif-item ${n.unread?'unread':''}">
        <div class="notif-icon" style="background:${n.iconBg}"><i class="fas ${n.icon}" style="color:${n.iconColor}"></i></div>
        <div class="notif-body">
          <div class="title">${n.title}</div>
          <div class="msg">${n.msg}</div>
          <div class="time">${n.time}</div>
        </div>
        ${n.unread ? '<div class="unread-dot"></div>' : ''}
      </div>
    `).join('');
  },

  rankBadge(n) {
    if(n===1) return `<div class="rank-num rank-gold">1</div>`;
    if(n===2) return `<div class="rank-num rank-silver">2</div>`;
    if(n===3) return `<div class="rank-num rank-bronze">3</div>`;
    return `<div class="rank-num rank-plain">${n}</div>`;
  },
  atsBadge(score) { return score>=80?'badge-success':score>=60?'badge-warning':'badge-danger'; },
  statusBadge(status) {
    const map = { Shortlisted:'badge-success', Reviewing:'badge-info', Pending:'badge-warning', Rejected:'badge-danger' };
    return `<span class="badge ${map[status]||'badge-gray'}">${status}</span>`;
  },
  avatarColor(name) {
    const colors = ['#1260cc','#7c3aed','#0891b2','#047857','#be185d','#b45309','#dc2626','#065f46'];
    let h = 0; for(let c of name) h = c.charCodeAt(0) + h*31;
    return colors[Math.abs(h) % colors.length];
  }
};

// ── Charts ────────────────────────────────────────────────────
const Charts = {
  instances: {},

  destroy(id) { if(this.instances[id]) { this.instances[id].destroy(); delete this.instances[id]; } },

  create(id, config) {
    this.destroy(id);
    const ctx = document.getElementById(id);
    if (!ctx) return;
    this.instances[id] = new Chart(ctx, config);
  },

  defaults: {
    plugins: { legend: { labels: { font:{ family:'DM Sans', size:12 }, padding:14 } } },
    scales: {
      y: { grid: { color:'#f0f4f9' }, ticks: { font:{ family:'DM Sans', size:12 } } },
      x: { grid: { display:false },   ticks: { font:{ family:'DM Sans', size:12 } } }
    }
  },

  initCandidateCharts(score) {
    // ATS score donut — real data driven
    const s = score || (DB.currentUser && DB.currentUser.ats_score) || 0;
    this.create('cand-ats-mini', {
      type: 'doughnut',
      data: {
        labels: ['Score', 'Remaining'],
        datasets: [{ data: [s, 100-s], backgroundColor: ['#1260cc','#e6edf7'], borderWidth: 0, cutout:'78%' }]
      },
      options: { responsive:true, plugins:{ legend:{display:false}, tooltip:{enabled:false} } }
    });
    // NOTE: Profile Views timeline chart is now rendered with REAL API data
    // inside fetchCandidateStats() — do NOT add it here to avoid overwriting real data.
  },


  initAdminCharts() {
    // Charts are now fully driven by fetchAdminStats() — no hardcoded data
  },

  initAdminMiniCharts() {
    // Driven by fetchAdminStats() real data
  },

  initAnalyticsCharts(portal) {
    // All analytics charts are driven by fetchAdminStats() / fetchCandidateStats() real data
    // They will be populated when the API response arrives — no hardcoded data
  }
};

// ── Actions ───────────────────────────────────────────────────
function applyJob(id) {
  if (!DB.currentUser) return Toast.show('Please login first', 'warning');
  const job = DB.jobs.find(j => j.id === id);
  if (job) {
    fetch('/api/apply', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id: DB.currentUser.id, job_id: id, match_score: job.match})
    }).then(r=>r.json()).then(data => {
        if(data.success) {
            Toast.show(`Application submitted for ${job.title} at ${job.company}! 🚀`, 'success');
            job.applicants++;
        } else {
            Toast.show(data.message, 'warning');
        }
    });
  }
}

function editJob(id) {
  const job = DB.jobs.find(j => j.id === id);
  if (!job) return;
  document.getElementById('edit-job-title').value    = job.title;
  document.getElementById('edit-job-company').value  = job.company;
  document.getElementById('edit-job-location').value = job.location;
  document.getElementById('edit-job-type').value     = job.type;
  document.getElementById('edit-job-salary').value   = job.salary;
  document.getElementById('edit-job-skills').value   = job.skills.join(', ');
  document.getElementById('edit-job-id').value       = id;
  Modal.open('edit-job-modal');
}

function saveEditJob() {
  const id      = parseInt(document.getElementById('edit-job-id').value);
  const title   = document.getElementById('edit-job-title').value.trim();
  const company = document.getElementById('edit-job-company').value.trim();
  const location= document.getElementById('edit-job-location').value.trim();
  const type    = document.getElementById('edit-job-type').value;
  const salary  = document.getElementById('edit-job-salary').value.trim();
  const skills  = document.getElementById('edit-job-skills').value.trim();
  
  if (!title||!company) { Toast.show('Title and company are required.','warning'); return; }
  
  fetch(`/api/admin/jobs/${id}`, {
    method: 'PUT', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title, company, location, type, salary, skills, description: ''})
  }).then(r => r.json()).then(data => {
    if (data.success) {
      // Update local store
      const job = DB.jobs.find(j => j.id === id);
      if (job) {
        job.title = title; job.company = company; job.location = location;
        job.type = type; job.salary = salary;
        job.skills = skills.split(',').map(s => s.trim()).filter(Boolean);
      }
      Modal.close('edit-job-modal');
      UI.renderJobCards('admin-jobs-grid', DB.jobs, false);
      Toast.show('Job updated successfully!', 'success');
    } else {
      Toast.show('Failed to update job.', 'error');
    }
  }).catch(() => Toast.show('Server error.', 'error'));
}

function deleteJob(id) {
  if (!confirm('Are you sure you want to delete this job?')) return;
  fetch(`/api/admin/delete_job/${id}`, { method: 'DELETE' }).then(r=>r.json()).then(res => {
    if(res.success) {
      DB.jobs = DB.jobs.filter(j => j.id !== id);
      UI.renderJobCards('admin-jobs-grid', DB.jobs, false);
      Toast.show('Job deleted.', 'info');
    }
  });
}

function postJob() {
  const title    = document.getElementById('new-job-title').value.trim();
  const company  = document.getElementById('new-job-company').value.trim();
  const location = document.getElementById('new-job-location').value.trim();
  const type     = document.getElementById('new-job-type').value;
  const salary   = document.getElementById('new-job-salary').value.trim();
  const skills   = document.getElementById('new-job-skills').value.trim();
  const desc     = document.getElementById('new-job-desc').value.trim();

  if (!title||!company||!location||!salary) { Toast.show('Please fill in all required fields.','warning'); return; }

  fetch('/api/admin/jobs', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({title, company, location, type, salary, skills, description: desc})
  }).then(r=>r.json()).then(data => {
      Modal.close('post-job-modal');
      // Reset form
      ['new-job-title','new-job-company','new-job-location','new-job-salary','new-job-skills','new-job-desc'].forEach(id=>{
        const el = document.getElementById(id); if(el) el.value='';
      });
      Toast.show(`"${title}" posted successfully! <i class="fa-solid fa-wand-magic-sparkles"></i>`, 'success');
      fetchJobsFromServer(); // Refresh live jobs
  });
}

function viewCandidate(id) {
  const c = DB.candidates.find(x => x.id === id);
  if (!c) return;
  
  // Avatar initials
  const avatarEl = document.getElementById('modal-cand-avatar');
  if (avatarEl) {
    avatarEl.textContent = c.name.slice(0,2).toUpperCase();
    avatarEl.style.background = UI.avatarColor(c.name);
  }
  
  document.getElementById('modal-cand-name').textContent    = c.name;
  document.getElementById('modal-cand-email').textContent   = c.email;
  document.getElementById('modal-cand-degree').textContent  = `Applied for: ${c.job}`;
  document.getElementById('modal-cand-job').textContent     = c.job;
  document.getElementById('modal-cand-exp').textContent     = c.exp || 'Fresher';
  document.getElementById('modal-cand-ats').textContent     = c.ats + '/100';
  document.getElementById('modal-cand-match').textContent   = c.match + '%';
  document.getElementById('modal-cand-status').innerHTML    = UI.statusBadge(c.status);
  document.getElementById('modal-cand-skills').innerHTML    = c.skills.length
    ? c.skills.map(s=>`<span class="skill-tag skill-neutral">${s}</span>`).join('')
    : '<span class="text-muted text-sm">No skills extracted yet</span>';
  
  // Wire action buttons to real API
  const btnShortlist = document.getElementById('modal-btn-shortlist');
  const btnReject    = document.getElementById('modal-btn-reject');
  if (btnShortlist) {
    btnShortlist.onclick = () => {
      updateCandidateStatus(id, 'Shortlisted');
      document.getElementById('modal-cand-status').innerHTML = UI.statusBadge('Shortlisted');
      Modal.close('view-cand-modal');
    };
  }
  if (btnReject) {
    btnReject.onclick = () => {
      updateCandidateStatus(id, 'Rejected');
      document.getElementById('modal-cand-status').innerHTML = UI.statusBadge('Rejected');
      Modal.close('view-cand-modal');
    };
  }
  
  Modal.open('view-cand-modal');
}


function viewJobRankings(jobId) {
  const job = DB.jobs.find(j => j.id === jobId);
  Sidebar.setActive(document.querySelector('#sb-admin .sb-item[data-section="rankings"]'));
  Router.inner('admin','rankings');
  UI.renderRankingsTable(jobId);
  if (job) Toast.show(`Showing rankings for: ${job.title}`, 'info');
}

function exportCSV() {
  const headers = ['Rank','Name','Email','Degree','Job','ATS','Match','Experience','Status'];
  const rows = DB.candidates.sort((a,b)=>b.ats-a.ats).map((c,i)=>[i+1,c.name,c.email,c.degree,c.job,c.ats+'%',c.match+'%',c.exp,c.status]);
  const csv = [headers,...rows].map(r=>r.join(',')).join('\n');
  const blob = new Blob([csv], {type:'text/csv'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href=url; a.download='candidates.csv'; a.click();
  URL.revokeObjectURL(url);
  Toast.show('CSV exported successfully!','success');
}

function searchCandidates(val) {
  const q = val.toLowerCase();
  const filtered = DB.candidates.filter(c => c.name.toLowerCase().includes(q) || c.job.toLowerCase().includes(q) || c.email.toLowerCase().includes(q));
  const tbody = document.getElementById('candidates-tbody');
  if (!tbody) return;
  if (!q) { UI.renderCandidatesTable(); return; }
  // Temporarily swap
  const saved = DB.candidates;
  const bak = DB.candidates;
  DB.candidates = filtered;
  UI.renderCandidatesTable();
  DB.candidates = bak;
}

function filterJobs(portal) {
  const loc  = document.getElementById(`${portal}-filter-loc`).value;
  const type = document.getElementById(`${portal}-filter-type`).value;
  let jobs = [...DB.jobs];
  if (loc && loc !== 'All') jobs = jobs.filter(j => j.location.includes(loc) || (loc==='Remote'&&j.type==='Contract'));
  if (type && type !== 'All') jobs = jobs.filter(j => j.type === type);
  const isCand = portal === 'cand';
  UI.renderJobCards(isCand ? 'cand-jobs-grid' : 'admin-jobs-grid', jobs, isCand);
}

function resetFilters(portal) {
  document.getElementById(`${portal}-filter-loc`).value  = 'All';
  document.getElementById(`${portal}-filter-type`).value = 'All';
  const isCand = portal === 'cand';
  UI.renderJobCards(isCand ? 'cand-jobs-grid' : 'admin-jobs-grid', DB.jobs, isCand);
}

function saveProfile(portal) {
  if (!DB.currentUser) return;
  
  let name;
  if (portal === 'cand') {
    const fname = (document.getElementById('cand-profile-name')?.value || '').trim();
    const lname = (document.getElementById('cand-profile-lname')?.value || '').trim();
    name = lname ? `${fname} ${lname}` : fname;
  } else {
    name = (document.getElementById('admin-profile-name')?.value || '').trim();
  }
  
  const data = {
    name,
    email:     (document.getElementById(`${portal}-profile-email`)?.value || '').trim(),
    phone:     (document.getElementById(`${portal}-profile-phone`)?.value || '').trim(),
    location:  (document.getElementById(`${portal}-profile-loc`)?.value || '').trim(),
    linkedin:  (document.getElementById(`${portal}-profile-link`)?.value || '').trim(),
    github:    (document.getElementById(`${portal}-profile-git`)?.value || '').trim(),
    summary:   (document.getElementById(`${portal}-profile-sum`)?.value || '').trim(),
    education: (document.getElementById(`${portal}-profile-edu`)?.value || '').trim()
  };
  
  if (!data.name) { Toast.show('Name cannot be empty.','warning'); return; }
  
  fetch(`/api/users/${DB.currentUser.id}/profile`, {
    method: 'PUT', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).then(r=>r.json()).then(res => {
    if(res.success) {
      // Update local store and all UI elements
      Object.assign(DB.currentUser, data);
      DB.currentUser.avatar = data.name.slice(0,2).toUpperCase();
      Auth.setupPortal(DB.currentUser);
      // Also update analysis/profile display
      setEl('profile-name', data.name);
      setEl('profile-email', data.email);
      setEl('profile-phone', data.phone);
      setEl('profile-location', data.location);
      setEl('profile-linkedin', data.linkedin);
      setEl('profile-github', data.github);
      setEl('profile-summary', data.summary);
      setEl('profile-education', data.education);
      Toast.show('Profile saved successfully! ✓','success');
    } else { Toast.show('Failed to save profile.','error'); }
  }).catch(() => Toast.show('Server error.','error'));
}


function changePwd(portal) {
  const cur  = document.getElementById(`${portal}-cur-pwd`).value;
  const nw   = document.getElementById(`${portal}-new-pwd`).value;
  const conf = document.getElementById(`${portal}-conf-pwd`).value;
  if (!cur||!nw||!conf) { Toast.show('Please fill in all password fields.','warning'); return; }
  if (nw !== conf) { Toast.show('New passwords do not match!','error'); return; }
  if (nw.length < 8) { Toast.show('Password must be at least 8 characters.','warning'); return; }
  
  fetch('/api/auth/change_password', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ current_password: cur, new_password: nw })
  }).then(r => r.json()).then(data => {
    if (data.success) {
      Toast.show('Password changed successfully! 🔒', 'success');
      ['cur-pwd','new-pwd','conf-pwd'].forEach(s => { const el=document.getElementById(`${portal}-${s}`); if(el) el.value=''; });
    } else {
      Toast.show(data.message || 'Failed to change password.', 'error');
    }
  }).catch(() => Toast.show('Server error.', 'error'));
}

function saveSettings() {
  const settings = {
    newAlerts: document.getElementById('set-new-alerts')?.checked,
    emailShortlist: document.getElementById('set-email-shortlist')?.checked,
    weeklyReport: document.getElementById('set-weekly-report')?.checked,
    autoRank: document.getElementById('set-auto-rank')?.checked,
    strictAts: document.getElementById('set-strict-ats')?.checked,
    softSkills: document.getElementById('set-soft-skills')?.checked,
    tfa: document.getElementById('set-2fa')?.checked,
    darkMode: document.getElementById('set-dark-mode')?.checked
  };
  localStorage.setItem('hireai_settings', JSON.stringify(settings));
  Toast.show('Settings saved to device.', 'success');
}

function switchSettingTab(tab, el) {
  if (el && el.closest('.settings-nav')) {
    el.closest('.settings-nav').querySelectorAll('.settings-nav-item').forEach(i => i.classList.remove('active'));
    el.classList.add('active');
  }
  
  const portal = el ? el.closest('[data-portal]') : document;
  if (portal) {
    portal.querySelectorAll('.set-tab-pane').forEach(p => p.classList.add('hidden'));
  } else {
    document.querySelectorAll('.set-tab-pane').forEach(p => p.classList.add('hidden'));
  }
  
  const target = document.getElementById('set-tab-' + tab);
  if (target) target.classList.remove('hidden');
}

function toggleDarkMode(isDark) {
  if (isDark) {
    document.body.classList.add('dark-mode');
  } else {
    document.body.classList.remove('dark-mode');
  }
  saveSettings();
}

function loadSettings() {
  const saved = localStorage.getItem('hireai_settings');
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      if (parsed.newAlerts !== undefined) { const el = document.getElementById('set-new-alerts'); if(el) el.checked = parsed.newAlerts; }
      if (parsed.emailShortlist !== undefined) { const el = document.getElementById('set-email-shortlist'); if(el) el.checked = parsed.emailShortlist; }
      if (parsed.weeklyReport !== undefined) { const el = document.getElementById('set-weekly-report'); if(el) el.checked = parsed.weeklyReport; }
      if (parsed.autoRank !== undefined) { const el = document.getElementById('set-auto-rank'); if(el) el.checked = parsed.autoRank; }
      if (parsed.strictAts !== undefined) { const el = document.getElementById('set-strict-ats'); if(el) el.checked = parsed.strictAts; }
      if (parsed.softSkills !== undefined) { const el = document.getElementById('set-soft-skills'); if(el) el.checked = parsed.softSkills; }
      if (parsed.tfa !== undefined) { const el = document.getElementById('set-2fa'); if(el) el.checked = parsed.tfa; }
      if (parsed.darkMode !== undefined) { 
        const el = document.getElementById('set-dark-mode'); 
        if(el) el.checked = parsed.darkMode; 
        if(parsed.darkMode) document.body.classList.add('dark-mode'); 
      }
    } catch(e){}
  }
}
// Load on startup
document.addEventListener('DOMContentLoaded', loadSettings);

function markAllRead(portal) {
  if (!DB.currentUser) return;
  fetch(`/api/notifications/${DB.currentUser.id}/read`, { method: 'POST' })
  .then(r=>r.json()).then(res => {
    if(res.success) {
      DB.notifications.forEach(n => n.unread = false);
      UI.renderNotifications(portal); // will fetch fresh list
      updateSidebarBadges();
      Toast.show('All notifications marked as read.','info');
    }
  });
}

function viewMatchedJobs() {
  Router.inner('cand','jobs');
  Sidebar.setActive(document.querySelector('#sb-cand [data-section=jobs]'));
  
  // Real logic: The ML API already returns the Top 10 matched jobs. Show them all.
  const matchedJobs = DB.jobs;
  UI.renderJobCards('cand-jobs-grid', matchedJobs, true);
  
  Toast.show(`Showing top ${matchedJobs.length} AI-matched jobs for your profile!`, 'info');
}

function triggerReupload() {
  Router.inner('cand','upload');
  Sidebar.setActive(document.querySelector('#sb-cand [data-section=upload]'));
  // Trigger file selection natively after a short delay
  setTimeout(() => {
    document.getElementById('resume-file-input').click();
  }, 50);
}

function resumeUpload(e) {
  const files = e.target.files;
  if (!files.length) return;
  const file = files[0];
  const allowed = ['application/pdf','application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  if (!allowed.includes(file.type)) { Toast.show('Only PDF, DOC, DOCX files allowed.','error'); return; }
  if (file.size > 5*1024*1024) { Toast.show('File must be under 5MB.','error'); return; }

  const isWord = file.name.toLowerCase().endsWith('.docx') || file.name.toLowerCase().endsWith('.doc');
  const iconClass = isWord ? 'fas fa-file-word' : 'fas fa-file-pdf';
  const iconColor = isWord ? '#2563eb' : '#dc2626'; // blue for Word, red for PDF
  const iconBg = isWord ? '#dbeafe' : '#fee2e2';

  const list = document.getElementById('upload-list');
  const item = document.createElement('div');
  item.className = 'upload-item';
  item.innerHTML = `
    <div class="upload-item-icon" style="background:${iconBg}"><i class="${iconClass}" style="color:${iconColor}"></i></div>
    <div class="upload-item-body">
      <div class="upload-item-name">${file.name}</div>
      <div class="upload-item-meta">${(file.size/1024).toFixed(0)} KB · Uploading...</div>
      <div class="progress"><div class="progress-bar" id="up-prog" style="width:0%;background:#1260cc"></div></div>
    </div>
    <span class="badge badge-info">Uploading...</span>
  `;
  list.prepend(item);

  const formData = new FormData();
  formData.append('resume', file);
  if (DB.currentUser) formData.append('user_id', DB.currentUser.id);
  
  const bar = item.querySelector('#up-prog');
  const badge = item.querySelector('.badge');
  
  bar.style.width = '40%';
  Toast.show(`Uploading "${file.name}" to AI server...`,'info');

  fetch('/api/upload_resume', {
      method: 'POST',
      body: formData
  })
  .then(res => res.json())
  .then(data => {
      if(data.error) {
          badge.className='badge badge-danger'; badge.innerHTML='<i class="fas fa-times"></i> Error';
          Toast.show(data.error, 'error');
          return;
      }
      bar.style.width = '100%';
      bar.style.background='#16a34a';
      badge.className='badge badge-success'; badge.innerHTML='<i class="fas fa-check"></i> Analyzed';
      Toast.show(`Resume parsed! ATS Score: ${data.data.ats_score}/100 <i class="fa-solid fa-wand-magic-sparkles"></i>`, 'success');
      
      // Update current user's data in memory so the ML pipeline works everywhere
      if(DB.currentUser) {
          DB.currentUser.ats_score = data.data.ats_score;
          DB.currentUser.skills = data.data.skills.join(',');
          fetchCandidateStats(DB.currentUser.id);
      }
      // Force-refresh ML job matches (invalidates cache since skills changed)
      _mlJobsCache = null;
      _mlJobsCacheKey = '';
      fetchJobsFromServer(true);
  })
  .catch(err => {
      badge.className='badge badge-danger'; badge.innerHTML='<i class="fas fa-times"></i> Error';
      Toast.show('Error connecting to AI Server. Is it running?', 'error');
  });
}

function fetchJobs(skills) {
  fetch('/api/match_jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skills: skills })
  })
  .then(res => res.json())
  .then(data => {
      if(data.success && data.jobs.length > 0) {
          Toast.show(`AI found ${data.jobs.length} highly matched jobs!`, 'info');
          // Map backend jobs to frontend UI schema
          const mappedJobs = data.jobs.map(j => ({
              id: j.id,
              title: j.title,
              company: j.company,
              location: 'Remote/Office',
              type: 'Full-time',
              salary: 'To be discussed',
              skills: skills.slice(0, 3), // Show matching skills
              applicants: Math.floor(Math.random() * 50),
              status: 'Active',
              match: j.match_percentage,
              color: '#eff6ff', textColor: '#1e40af',
              logo: j.company.substring(0, 2).toUpperCase()
          }));
          UI.renderJobCards('cand-jobs-grid', mappedJobs, true);
      }
  })
  .catch(err => console.error(err));
}

function handleDrop(e, zone) {
  e.preventDefault();
  zone.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length) {
    const fakeInput = { target: { files } };
    resumeUpload(fakeInput);
  }
}

// Topbar search
function topbarSearch(val, portal) {
  if (!val.trim()) return;
  if (portal === 'admin') searchCandidates(val);
  Toast.show(`Searching for "${val}"...`,'info');
}

// ── API Fetchers (World-Class Live Data) ────────────────────────────────
const JOB_COLORS = [
  {color:'#eff6ff',textColor:'#1e40af'},{color:'#f0fdf4',textColor:'#166534'},
  {color:'#fff7ed',textColor:'#9a3412'},{color:'#fdf2f8',textColor:'#86198f'},
  {color:'#f5f3ff',textColor:'#6d28d9'},{color:'#fff1f2',textColor:'#9f1239'},
  {color:'#ecfdf5',textColor:'#065f46'},{color:'#fffbeb',textColor:'#92400e'},
];

// ── ML Job Cache (avoids re-running expensive ML pipeline) ───
let _mlJobsCache = null;
let _mlJobsCacheKey = '';

function fetchJobsFromServer(forceMLRefresh = false) {
  // If the user is a candidate with parsed skills, use the REAL ML pipeline!
  if (DB.currentUser && DB.currentUser.role !== 'hr' && DB.currentUser.skills) {
    const userSkills = DB.currentUser.skills.split(',').map(s => s.trim()).filter(Boolean);
    const cacheKey = userSkills.sort().join('|');

    // Use cached ML results unless explicitly forced or skills changed
    if (!forceMLRefresh && _mlJobsCache && _mlJobsCacheKey === cacheKey) {
      DB.jobs = _mlJobsCache;
      UI.renderJobCards('cand-jobs-grid', DB.jobs, true);
      setEl('cand-jobs-count', `${DB.jobs.length} Matching Jobs Found`);
      updateSidebarBadges();
    } else {
      fetch('/api/match_jobs', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ skills: userSkills })
      })
      .then(r => r.json())
      .then(data => {
          if (data.success && data.jobs) {
              DB.jobs = data.jobs.map((j, i) => ({
                  id: j.id, title: j.title, company: j.company, location: j.location || 'Remote/Office',
                  type: j.type || 'Full-time', salary: j.salary || 'To be discussed',
                  skills: j.skills ? j.skills.split(',').map(s=>s.trim()) : [],
                  description: j.description, status: j.status || 'Active',
                  applicants: 0, match: j.match_percentage,
                  ...JOB_COLORS[i % JOB_COLORS.length],
                  logo: (j.company||'??').substring(0,2).toUpperCase()
              }));
              DB.jobs.sort((a, b) => b.match - a.match);
              _mlJobsCache = DB.jobs;
              _mlJobsCacheKey = cacheKey;
              UI.renderJobCards('cand-jobs-grid', DB.jobs, true);
              setEl('cand-jobs-count', `${DB.jobs.length} Matching Jobs Found`);
              updateSidebarBadges();
          }
      }).catch(err => console.error("Error fetching ML job matches:", err));
    }
  }

  // Fetch all jobs for the Admin view (lightweight, no ML)
  fetch('/api/admin/jobs').then(r=>r.json()).then(data=>{
    const adminJobs = data.map((j,i) => {
      const jobSkills = j.skills ? j.skills.split(',').map(s=>s.trim()) : [];
      return {
        id: j.id, title: j.title, company: j.company, location: j.location,
        type: j.type || 'Full-time', salary: j.salary,
        skills: jobSkills, description: j.description, status: j.status || 'Active',
        applicants: 0, match: 50,
        ...JOB_COLORS[i % JOB_COLORS.length],
        logo: (j.company||'??').substring(0,2).toUpperCase()
      };
    });
    if (!DB.currentUser || DB.currentUser.role === 'hr' || !DB.currentUser.skills) {
       DB.jobs = adminJobs;
       UI.renderJobCards('cand-jobs-grid', DB.jobs, true);
       setEl('cand-jobs-count', `${DB.jobs.length} Matching Jobs Found`);
    }
    UI.renderJobCards('admin-jobs-grid', adminJobs, false);
    updateSidebarBadges();
  });
}


function fetchCandidatesFromServer() {
  fetch('/api/admin/candidates').then(r=>r.json()).then(data=>{
    DB.candidates = data.map(c => ({
      id: c.app_id, name: c.name, email: c.email,
      degree: 'See Profile', job: c.job,
      ats: c.ats_score || 0, match: c.match_score || 0,
      exp: 'Fresher', sim: (c.match_score||0)/100,
      status: c.status,
      outlier_flag:   c.outlier_flag   || false,
      outlier_reason: c.outlier_reason || '',
      cluster_label:  c.cluster_label  || 'Unclustered',
      skills: c.skills ? c.skills.split(',').map(s=>s.trim()).filter(Boolean) : []
    }));
    UI.renderCandidatesTable();
    UI.renderRankingsTable();

    // ── Update HR filter tab counts with real numbers ──
    const all         = DB.candidates.length;
    const shortlisted = DB.candidates.filter(c => c.status === 'Shortlisted').length;
    const reviewing   = DB.candidates.filter(c => c.status === 'Reviewing').length;
    const pending     = DB.candidates.filter(c => c.status === 'Pending').length;
    const rejected    = DB.candidates.filter(c => c.status === 'Rejected').length;
    setEl('tab-count-all',         all);
    setEl('tab-count-shortlisted', shortlisted);
    setEl('tab-count-reviewing',   reviewing + pending);   // Reviewing + Pending combined
    setEl('tab-count-rejected',    rejected);
    const outlierCount = DB.candidates.filter(c => c.outlier_flag).length;
    setEl('tab-count-outliers', outlierCount);
    // Render cluster view if it exists in DOM
    renderClusterView();

    updateSidebarBadges();
    
    // Populate recent applications on HR Dashboard (top 5 by ID desc as proxy for recent)
    const recentTbody = document.getElementById('admin-dash-recent-tbody');
    if (recentTbody && DB.candidates) {
      const recentCands = [...DB.candidates].sort((a,b) => b.id - a.id).slice(0, 5);
      recentTbody.innerHTML = recentCands.map(c => `
        <tr>
          <td><div class="fw-600">${c.name}</div><div class="text-xs text-muted">${c.email}</div></td>
          <td>${c.job}</td>
          <td><span class="badge ${c.ats >= 80 ? 'badge-success' : (c.ats >= 50 ? 'badge-warning' : 'badge-danger')}">${c.ats}</span></td>
          <td>${UI.statusBadge(c.status)}</td>
          <td><button class="btn btn-sm btn-primary" onclick="viewCandidate(${c.id})">View</button></td>
        </tr>
      `).join('');
    }
  });
}

// Pull Notifications
function fetchNotificationsFromServer(userId) {
  fetch(`/api/notifications/${userId}`).then(r=>r.json()).then(data=>{
    DB.notifications = data.map(n => ({
      id: n.id,
      title: n.title,
      msg: n.message,
      time: n.created_at,
      icon: n.type === 'success' ? 'fa-check-circle' : (n.type === 'error' ? 'fa-times-circle' : 'fa-bell'),
      iconBg: n.type === 'success' ? '#dcfce7' : (n.type === 'error' ? '#fee2e2' : '#eff6ff'),
      iconColor: n.type === 'success' ? '#16a34a' : (n.type === 'error' ? '#dc2626' : '#1e40af'),
      unread: n.is_read === 0
    }));
    UI.renderNotifications(DB.currentUser?.role === 'hr' ? 'admin' : 'cand');
    updateSidebarBadges();
  });
}

// Pull ALL live stats and update admin dashboard numbers
function fetchAdminStats() {
  fetch('/api/admin/stats').then(r=>r.json()).then(d=>{
    // Stat cards (dashboard KPIs)
    setEl('stat-total-applicants', d.total_applicants);
    setEl('stat-resumes-analyzed', d.resumes_analyzed);
    setEl('stat-shortlisted',      d.shortlisted);
    setEl('stat-active-jobs',      d.active_jobs);
    setEl('stat-avg-ats',          d.avg_ats_score);
    setEl('stat-reviewing',        d.reviewing);
    // NOTE: tab counts (All/Shortlisted/Reviewing/Rejected) are set by
    // fetchCandidatesFromServer() which uses the real joined candidate list.

    // Charts with real data
    const skillLabels = d.top_skills.map(x=>x.skill);
    const skillCounts = d.top_skills.map(x=>x.count);

    Charts.create('admin-skills-donut', {
      type:'doughnut',
      data:{ labels: skillLabels,
        datasets:[{ data: skillCounts,
          backgroundColor:['#1260cc','#00c9a7','#16a34a','#d97706','#7c3aed','#94a3b8','#e11d48','#0891b2'],
          borderWidth:3, borderColor:'#fff' }] },
      options:{ responsive:true, plugins:{ legend:{ position:'bottom', labels:{ font:{family:'DM Sans',size:12}, padding:10 }}}, cutout:'60%' }
    });

    Charts.create('admin-app-trend', {
      type:'bar',
      data:{ labels:['Shortlisted','Reviewing','Pending','Rejected'],
        datasets:[{ label:'Candidates', data:[d.shortlisted,d.reviewing,d.pending,d.rejected],
          backgroundColor:['#16a34a','#1260cc','#d97706','#dc2626'], borderRadius:6 }] },
      options:{ responsive:true, plugins:{legend:{display:false}}, scales:{ y:{beginAtZero:true,grid:{color:'#f0f4f9'}}, x:{grid:{display:false}} }}
    });

    // Analytics charts
    const roleLabels = d.apps_by_role.map(x=>x.role);
    const roleCounts = d.apps_by_role.map(x=>x.count);
    Charts.create('admin-role-pie', {
      type:'pie',
      data:{ labels:roleLabels,
        datasets:[{ data:roleCounts, backgroundColor:['#1260cc','#00c9a7','#16a34a','#d97706','#7c3aed','#94a3b8'], borderWidth:3, borderColor:'#fff' }] },
      options:{ responsive:true, plugins:{ legend:{ position:'bottom', labels:{ font:{family:'DM Sans',size:12}, padding:10 }}}}
    });
    Charts.create('admin-skills-bar', {
      type:'bar',
      data:{ labels:skillLabels,
        datasets:[{ label:'Candidates with skill', data:skillCounts, backgroundColor:'#1260cc', borderRadius:6 }] },
      options:{ indexAxis:'y', responsive:true, plugins:{legend:{display:false}}, scales:{ x:{beginAtZero:true,grid:{color:'#f0f4f9'}}, y:{grid:{display:false}} }}
    });
    Charts.create('admin-status-funnel', {
      type:'doughnut',
      data:{ labels:['Shortlisted','Reviewing','Pending','Rejected'],
        datasets:[{ data:[d.shortlisted,d.reviewing,d.pending,d.rejected],
          backgroundColor:['#16a34a','#1260cc','#d97706','#dc2626'], borderWidth:3, borderColor:'#fff' }] },
      options:{ responsive:true, plugins:{ legend:{ position:'bottom', labels:{ font:{family:'DM Sans',size:12}, padding:10 }}}, cutout:'65%' }
    });
    Charts.create('admin-ats-dist', {
      type:'bar',
      data:{
        labels:['0–20','21–40','41–60','61–70','71–80','81–90','91–100'],
        datasets:[{
          label:'Candidates',
          data:d.ats_distribution,
          backgroundColor:['#fee2e2','#fecaca','#fed7aa','#fef08a','#bbf7d0','#6ee7b7','#00c9a7'],
          borderRadius:6
        }]
      },
      options:{ responsive:true, plugins:{legend:{display:false}}, scales:{ y:{beginAtZero:true,grid:{color:'#f0f4f9'}}, x:{grid:{display:false}} } }
    });
    Charts.create('admin-app-time', {
      type:'line',
      data:{
        labels:d.app_time.labels,
        datasets:[{
          label:'Total Applications',
          data:d.app_time.total,
          borderColor:'#1260cc', backgroundColor:'rgba(18,96,204,.1)',
          tension:.4, fill:true, pointBackgroundColor:'#1260cc'
        },{
          label:'Shortlisted',
          data:d.app_time.shortlisted,
          borderColor:'#00c9a7', backgroundColor:'rgba(0,201,167,.08)',
          tension:.4, fill:true, pointBackgroundColor:'#00c9a7'
        }]
      },
      options:{ responsive:true, plugins:{ legend:{ position:'top', labels:{ font:{family:'DM Sans',size:12}, padding:14 } } }, scales:{ y:{beginAtZero:true,grid:{color:'#f0f4f9'}}, x:{grid:{display:false}} } }
    });
    Charts.create('admin-hires', {
      type:'line',
      data:{
        labels: d.app_time.labels,
        datasets:[{
          label:'Shortlisted',
          data: d.app_time.shortlisted,
          borderColor:'#16a34a', backgroundColor:'rgba(22,163,74,.1)',
          tension:.4, fill:true, pointBackgroundColor:'#16a34a'
        }]
      },
      options:{ responsive:true, plugins:{legend:{display:false}}, scales:{ y:{beginAtZero:true,grid:{color:'#f0f4f9'}}, x:{grid:{display:false}} } }
    });

    // ── Analytics page stat cards (dynamic) ──
    // Avg ATS
    const avgAtsEl = document.querySelector('#admin-analytics .stat-value');
    if (avgAtsEl) avgAtsEl.textContent = d.avg_ats_score;
    
    // Bind all analytics stats by ID
    setEl('stat-analytics-avg-ats',      d.avg_ats_score);
    setEl('stat-analytics-top-skill',    d.top_skill_demanded || (d.top_skills[0]?.skill || 'Python'));
    setEl('stat-analytics-accept-rate',  d.acceptance_rate + '%');
    setEl('stat-analytics-active-jobs',  d.active_jobs);
    
    // Job postings header: "X active positions"
    const jobsHeader = document.getElementById('admin-jobs-header-count');
    if (jobsHeader) jobsHeader.textContent = `${d.active_jobs} active positions · ${d.reviewing} reviewing`;
    
    updateSidebarBadges();
  });
}


// Pull live candidate stats for the logged-in user
function fetchCandidateStats(userId) {
  fetch(`/api/candidate/stats/${userId}`).then(r=>r.json()).then(d=>{
    const score = d.ats_score || 0;
    // Stat cards
    setEl('cand-stat-ats',          score);
    setEl('cand-stat-skills',       d.skills_count || 0);
    // Real ML matched jobs count — use cached result count if available, else DB total
    const realMatchedCount = (_mlJobsCache && _mlJobsCache.length > 0) ? _mlJobsCache.length : (d.job_matches || 0);
    setEl('cand-stat-matches',      realMatchedCount);
    setEl('cand-stat-apps',         d.applications || 0);
    setEl('cand-analytics-stat-ats', score);
    // ATS display in welcome banner + mini donut + dashboard ATS
    setEl('cand-ats-display', score);
    setEl('ats-score-big-num', score);
    setEl('cand-ats-mini-num', score || '--');
    const svg = document.querySelector('.score-svg');
    if(svg) svg.setAttribute('data-score', score);
    

    // Profile Views — real from DB (0 means no HR has viewed your profile yet)
    const realViews = d.profile_views !== undefined ? d.profile_views : 0;
    const realWeekly = d.profile_views_weekly !== undefined ? d.profile_views_weekly : 0;
    setEl('cand-stat-views', realViews);
    setEl('cand-stat-views-weekly', realWeekly > 0 ? `+${realWeekly} this week` : 'No views yet');
    setEl('cand-analytics-views', realViews);
    setEl('cand-analytics-views-weekly', realWeekly > 0 ? `+${realWeekly}` : '0');
    setEl('cand-analytics-apps', d.applications || 0);
    setEl('cand-analytics-matches', realMatchedCount);

    // Matched keywords
    const atsMatchedContainer = document.getElementById('ats-matched-keywords');
    if(atsMatchedContainer && d.skills) {
      atsMatchedContainer.innerHTML = d.skills.map(s => `<span class="skill-tag skill-match">${s} ✓</span>`).join('');
    }
    
    // Missing keywords
    const missingContainer = document.getElementById('cand-missing-keywords');
    const missingCount = document.getElementById('cand-missing-count');
    if(missingContainer && d.missing_skills) {
      missingContainer.innerHTML = d.missing_skills.map(s => `<span class="skill-tag skill-missing">${s} ✗</span>`).join('');
      if(missingCount) missingCount.textContent = `${d.missing_skills.length} Missing`;
    }

    // Top 4 Jobs in Dashboard
    const jobsTbody = document.getElementById('cand-dash-jobs-tbody');
    if (jobsTbody && DB.jobs) {
      const topJobs = [...DB.jobs].sort((a,b) => b.match - a.match).slice(0, 4);
      jobsTbody.innerHTML = topJobs.map(j => `
        <tr>
          <td><strong>${j.title}</strong></td>
          <td>${j.company}</td>
          <td><span class="badge ${j.match >= 80 ? 'badge-success' : 'badge-warning'}">${j.match}%</span></td>
          <td><span class="badge badge-info">${j.type}</span></td>
          <td><button class="btn btn-sm btn-primary" onclick="applyJob(${j.id})">Apply</button></td>
        </tr>
      `).join('');
    }

    // ATS mini-donut
    Charts.create('cand-ats-mini', {
      type:'doughnut',
      data:{ labels:['Score','Remaining'],
        datasets:[{ data:[score, 100-score], backgroundColor:['#1260cc','#e6edf7'], borderWidth:0, cutout:'78%' }] },
      options:{ responsive:true, plugins:{ legend:{display:false}, tooltip:{enabled:false} }}
    });
    // Toggle new-user vs returning-user banners
    const hasResume = score > 0;
    const newBanner     = document.getElementById('new-user-banner');
    const returningBanner = document.getElementById('resume-upload-prompt');
    if(newBanner)       newBanner.classList.toggle('hidden', hasResume);
    if(returningBanner) returningBanner.classList.toggle('hidden', !hasResume);

    // Dynamic Candidate Charts
    if (d.market_trends) {
      const mt = d.market_trends;
      Charts.create('cand-ats-dist', {
        type:'bar',
        data:{
          labels:['0–20','21–40','41–60','61–70','71–80','81–90','91–100'],
          datasets:[{
            label:'Candidates',
            data:mt.ats_distribution,
            backgroundColor:['#fee2e2','#fecaca','#fed7aa','#fef08a','#bbf7d0','#6ee7b7','#00c9a7'],
            borderRadius:6
          }]
        },
        options:{ responsive:true, plugins:{legend:{display:false}}, scales:{ y:{beginAtZero:true,grid:{color:'#f0f4f9'}}, x:{grid:{display:false}} } }
      });

      Charts.create('cand-app-time', {
        type:'line',
        data:{
          labels:mt.app_time.labels,
          datasets:[{
            label:'Total Applications',
            data:mt.app_time.total,
            borderColor:'#1260cc', backgroundColor:'rgba(18,96,204,.1)',
            tension:.4, fill:true, pointBackgroundColor:'#1260cc'
          },{
            label:'Shortlisted',
            data:mt.app_time.shortlisted,
            borderColor:'#00c9a7', backgroundColor:'rgba(0,201,167,.08)',
            tension:.4, fill:true, pointBackgroundColor:'#00c9a7'
          }]
        },
        options:{ responsive:true, plugins:{ legend:{ position:'top', labels:{ font:{family:'DM Sans',size:12}, padding:14 } } }, scales:{ y:{beginAtZero:true,grid:{color:'#f0f4f9'}}, x:{grid:{display:false}} } }
      });

      const cSkillLabels = mt.top_skills.map(x=>x.skill);
      const cSkillCounts = mt.top_skills.map(x=>x.count);
      Charts.create('cand-skills-bar', {
        type:'bar',
        data:{
          labels:cSkillLabels,
          datasets:[{
            label:'Candidates with skill',
            data:cSkillCounts,
            backgroundColor:'#1260cc',
            borderRadius:6
          }]
        },
        options:{ indexAxis:'y', responsive:true, plugins:{legend:{display:false}}, scales:{ x:{beginAtZero:true,grid:{color:'#f0f4f9'}}, y:{grid:{display:false}} } }
      });
    }

    if (d.radar) {
      Charts.create('skills-radar', {
        type: 'radar',
        data: {
          labels: d.radar.labels,
          datasets: [{
            label:'Your Level',
            data: d.radar.levels,
            backgroundColor:'rgba(18,96,204,.15)',
            borderColor:'#1260cc', borderWidth:2,
            pointBackgroundColor:'#1260cc'
          },{
            label:'Required',
            data: d.radar.required,
            backgroundColor:'rgba(0,201,167,.12)',
            borderColor:'#00c9a7', borderWidth:2,
            pointBackgroundColor:'#00c9a7'
          }]
        },
        options: { responsive:true, plugins:{ legend:{ position:'bottom', labels:{ font:{family:'DM Sans',size:12}, padding:14 } } }, scales:{ r:{ grid:{color:'#e6edf7'}, ticks:{font:{size:11},stepSize:20}, suggestedMin:0, suggestedMax:100 } } }
      });
    }

      // Candidate analytics: role distribution from market_trends
      if (d.market_trends && d.market_trends.top_skills) {
        const roleLabels = d.market_trends.top_skills.slice(0,6).map(x => x.skill);
        const roleCounts = d.market_trends.top_skills.slice(0,6).map(x => x.count);
        Charts.create('cand-role-pie', {
          type:'pie',
          data:{ labels:roleLabels,
            datasets:[{ data:roleCounts, backgroundColor:['#1260cc','#00c9a7','#16a34a','#d97706','#7c3aed','#94a3b8'], borderWidth:3, borderColor:'#fff' }] },
          options:{ responsive:true, plugins:{ legend:{ position:'bottom', labels:{ font:{family:'DM Sans',size:12}, padding:10 }}}}
        });
      }

    // ── Render skill gaps (real proficiency bars) ──
    renderSkillGaps(d.skills || [], d.missing_skills || [], d.skill_demand_pct || {});

    
    // ── Render ATS page hero dynamically ──
    renderATSPage(score, d.skills || [], d.missing_skills || [], d.skills_count || 0);
    
    // ── Profile hero badge (ATS score) ──
    const profileAtsBadge = document.getElementById('profile-ats-badge');
    if (profileAtsBadge) profileAtsBadge.textContent = `ATS Score: ${score}/100`;
    
    // ── Profile Views This Week chart — REAL data from API ──
    const dayNames   = d.day_names   || ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    const viewsDaily = d.views_daily || [0,0,0,0,0,0,0];
    const appsDaily  = d.apps_daily  || [0,0,0,0,0,0,0];

    Charts.create('cand-timeline', {
      type: 'line',
      data: {
        labels: dayNames,
        datasets: [
          {
            label: 'Profile Views',
            data: viewsDaily,
            borderColor: '#1260cc',
            backgroundColor: 'rgba(18,96,204,.12)',
            tension: .4, fill: true, pointBackgroundColor: '#1260cc',
            pointRadius: 4
          },
          {
            label: 'Applications Sent',
            data: appsDaily,
            borderColor: '#00c9a7',
            backgroundColor: 'rgba(0,201,167,.08)',
            tension: .4, fill: true, pointBackgroundColor: '#00c9a7',
            pointRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top', labels: { font: { family: 'DM Sans', size: 12 }, padding: 14 } },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          y: { beginAtZero: true, precision: 0, grid: { color: '#f0f4f9' }, ticks: { stepSize: 1 } },
          x: { grid: { display: false } }
        }
      }
    });

    // Also update the ATS mini-donut (already done above but keep in sync)
    Charts.initCandidateCharts(score);

    updateSidebarBadges();

  });
}

// ── Render dynamic skill gap progress bars ──────────────────
function renderSkillGaps(skills, missingSkills, demandPct) {
  const container = document.getElementById('cand-skill-gaps');
  if (!container) return;

  // Combine candidate's own skills + missing skills (top 5 total)
  const allSkills = [...skills.slice(0, 3), ...missingSkills.slice(0, 2)];
  if (!allSkills.length) {
    container.innerHTML = '<p class="text-muted text-sm">Upload resume to see skill gaps.</p>';
    return;
  }

  container.innerHTML = allSkills.map(skill => {
    const isMissing  = missingSkills.includes(skill);
    // Real % = market demand from DB (how many candidates on platform have this skill)
    const realPct    = demandPct[skill] || demandPct[skill.toLowerCase()] || 0;
    const displayPct = isMissing ? 0 : (realPct > 0 ? realPct : 5);
    const color      = isMissing ? '#dc2626' : (displayPct >= 60 ? '#16a34a' : '#d97706');
    const label      = isMissing
      ? '<span style="font-size:10px;color:#dc2626;font-weight:600">⚠ Missing from your resume</span>'
      : `<span style="font-size:10px;color:#64748b">${displayPct}% market demand</span>`;

    return `
      <div style="margin-bottom:14px">
        <div style="display:flex;justify-content:space-between;align-items:baseline;font-size:13px;margin-bottom:4px">
          <div>
            <span style="font-weight:600">${skill}</span>
            <br>${label}
          </div>
          <span style="font-weight:700;color:${color};font-size:14px">${isMissing ? '0%' : displayPct + '%'}</span>
        </div>
        <div class="progress">
          <div class="progress-bar" style="width:${isMissing ? 2 : displayPct}%;background:${color};transition:width .8s ease"></div>
        </div>
      </div>`;
  }).join('');
}


// ── Render ATS page hero + breakdown bars dynamically ───────
function renderATSPage(score, skills, missingSkills, skillCount) {
  // Hero band text
  const atsHeading = document.getElementById('ats-hero-heading');
  const atsSubtext = document.getElementById('ats-hero-subtext');
  const atsBadgeMatched = document.getElementById('ats-badge-matched');
  const atsBadgeMissing = document.getElementById('ats-badge-missing');
  
  if (atsHeading) {
    const grade = score >= 80 ? 'Excellent' : score >= 65 ? 'Good' : score >= 50 ? 'Fair' : 'Needs Work';
    const emoji = score >= 80 ? '<i class="fa-solid fa-trophy"></i>' : score >= 65 ? '<i class="fa-solid fa-wand-magic-sparkles"></i>' : score >= 50 ? '<i class="fa-solid fa-thumbs-up"></i>' : '<i class="fa-solid fa-dumbbell"></i>';
    atsHeading.innerHTML = `${grade} ATS Score <span style="margin-left: 8px;">${emoji}</span>`;
  }
  if (atsSubtext) {
    atsSubtext.textContent = score >= 65
      ? `Your resume performs well. ${missingSkills.length > 0 ? 'Add ' + missingSkills.slice(0,2).join(', ') + ' to push above 90.' : 'Keep it up!'}`
      : `Add these skills to improve: ${missingSkills.slice(0,3).join(', ')}`;
  }
  if (atsBadgeMatched) atsBadgeMatched.textContent = `${skillCount} Keywords Matched`;
  if (atsBadgeMissing) atsBadgeMissing.textContent = `${missingSkills.length} Keywords Missing`;
  
  // SVG ring
  const svg = document.querySelector('.score-svg');
  if (svg) svg.setAttribute('data-score', score);
  setEl('ats-score-big-num', score);
  setTimeout(() => animateATSRings(), 200);
  
  // Breakdown progress bars (computed from ATS score)
  const bars = [
    { id:'ats-bar-keyword',    label:'Keyword Match',          pct: Math.min(100, Math.round(score * 1.05)) },
    { id:'ats-bar-skills',     label:'Skills Alignment',       pct: Math.min(100, Math.round(score * 0.97)) },
    { id:'ats-bar-experience', label:'Experience Match',       pct: Math.min(100, Math.round(score * 0.82)) },
    { id:'ats-bar-education',  label:'Education Fit',          pct: Math.min(100, Math.round(score * 1.1)) },
    { id:'ats-bar-format',     label:'Format & Readability',   pct: Math.min(100, Math.round(score * 0.78)) },
    { id:'ats-bar-contact',    label:'Contact Completeness',   pct: Math.min(100, score > 0 ? 85 : 0) }
  ];
  bars.forEach(b => {
    const el = document.getElementById(b.id);
    if (!el) return;
    const color = b.pct >= 80 ? 'linear-gradient(90deg,#16a34a,#4ade80)' : b.pct >= 60 ? 'linear-gradient(90deg,#d97706,#fbbf24)' : 'linear-gradient(90deg,#dc2626,#f87171)';
    const txtColor = b.pct >= 80 ? '#16a34a' : b.pct >= 60 ? '#d97706' : '#dc2626';
    el.innerHTML = `
      <div style="font-size:13px;font-weight:600;margin-bottom:10px;display:flex;justify-content:space-between">
        <span>${b.label}</span><span style="color:${txtColor};font-weight:700">${b.pct}%</span>
      </div>
      <div class="progress progress-lg"><div class="progress-bar" style="width:${b.pct}%;background:${color}"></div></div>`;
  });
}

// ── Render upload history from real user data ────────────────
function renderUploadHistory(user) {
  const list = document.getElementById('upload-list');
  if (!list) return;
  
  if (!user || !user.ats_score || user.ats_score === 0) {
    list.innerHTML = '<p class="text-muted text-sm" style="padding:16px">No resume uploaded yet.</p>';
    return;
  }
  
  const fname = user.resume_filename || `${(user.name||'Resume').replace(' ','_')}_Resume.pdf`;
  list.innerHTML = `
    <div class="upload-item">
      <div class="upload-item-icon" style="background:#fee2e2"><i class="fas fa-file-pdf" style="color:#dc2626;font-size:22px"></i></div>
      <div class="upload-item-body">
        <div class="upload-item-name">${fname}</div>
        <div class="upload-item-meta">Last analyzed · ATS Score: ${user.ats_score}/100</div>
        <div class="progress"><div class="progress-bar" style="width:100%;background:#16a34a"></div></div>
      </div>
      <span class="badge badge-success badge-lg"><i class="fas fa-check"></i> Analyzed</span>
      <button class="btn btn-sm btn-primary" onclick="Router.inner('cand','ats');Sidebar.setActive(document.querySelector('#sb-cand [data-section=ats]'))">View Score</button>
    </div>`;
}



// ── ML Pipeline Status ──────────────────────────────────
function loadMLPipelineStatus() {
  const btn = document.getElementById('pipeline-refresh-btn');
  if(btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...'; }

  fetch('/api/ml/status')
    .then(r => r.json())
    .then(data => {
      // Pipeline Status
      const isReady = data.status === 'ready';
      setEl('ml-pipeline-status', isReady ? '● Online' : '○ Not Trained');
      const statusEl = document.getElementById('ml-pipeline-status');
      if(statusEl) statusEl.style.color = isReady ? '#16a34a' : '#dc2626';
      setEl('ml-pipeline-status-sub', isReady ? 'All models loaded & operational' : 'Run training to activate');

      // TF-IDF Model
      const tfidf = data.models?.tfidf_recommender || {};
      setEl('ml-vocab-size', tfidf.vocab_size ? tfidf.vocab_size.toLocaleString() : '--');
      setEl('ml-tfidf-vocab', tfidf.vocab_size ? `${tfidf.vocab_size.toLocaleString()} terms` : '--');
      setEl('ml-corpus-size', tfidf.corpus_size || '--');
      setEl('ml-corpus-detail', `${tfidf.corpus_size || '800'} documents trained on`);
      setEl('ml-tfidf-corpus', `${tfidf.corpus_size || '--'} docs (resumes + job descriptions)`);

      const tfidfBadge = document.getElementById('ml-tfidf-badge');
      if(tfidfBadge) {
        tfidfBadge.className = tfidf.trained ? 'badge badge-success' : 'badge badge-danger';
        tfidfBadge.textContent = tfidf.trained ? '✓ Trained' : '✗ Not Trained';
      }

      // Hit rates
      const hr = tfidf.hit_rate || {};
      setEl('ml-tfidf-hit1', hr.hit_rate_top1 != null ? `${(hr.hit_rate_top1 * 100).toFixed(0)}%` : '--');
      setEl('ml-tfidf-hit3', hr.hit_rate_top3 != null ? `${(hr.hit_rate_top3 * 100).toFixed(0)}%` : '--');
      setEl('ml-tfidf-hit5', hr.hit_rate_top5 != null ? `${(hr.hit_rate_top5 * 100).toFixed(0)}%` : '--');
      setEl('ml-hit-rate', hr.hit_rate_top5 != null ? `${(hr.hit_rate_top5 * 100).toFixed(0)}%` : '--');

      // spaCy NER Model
      const ner = data.models?.spacy_ner || {};
      const nerBadge = document.getElementById('ml-ner-badge');
      if(nerBadge) {
        nerBadge.className = ner.trained ? 'badge badge-success' : 'badge badge-danger';
        nerBadge.textContent = ner.trained ? '✓ Trained' : '✗ Not Trained';
      }
      setEl('ml-ner-f1', ner.best_f1 != null ? `${(ner.best_f1 * 100).toFixed(1)}%` : '--');
      setEl('ml-ner-epochs', ner.epochs || '--');
      setEl('ml-ner-method', data.extraction_method || 'spaCy NER + Regex');
      setEl('ml-extraction-method', data.extraction_method || 'spaCy NER + Regex');

      // Dataset info
      const ds = data.dataset || {};
      setEl('ml-dataset-resumes', ds.num_resumes || '600');
      setEl('ml-dataset-jobs', ds.num_jobs || '200');
      setEl('ml-dataset-ner', ds.num_ner_samples || '~4,800');

      // Live jobs count from DB
      fetch('/api/admin/jobs').then(r=>r.json()).then(jobs => {
        setEl('ml-live-jobs', jobs.length || '--');
      });

      if(btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh Status'; }
    })
    .catch(err => {
      console.error('ML Pipeline status error:', err);
      setEl('ml-pipeline-status', '● Error');
      if(btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh Status'; }
    });
}


function fetchCandidateProfile(userId) {
  fetch(`/api/users/${userId}/profile`).then(r=>r.json()).then(d=>{

    // ── Toggle analysis empty state vs actual content ──
    const hasResume    = d.ats_score && d.ats_score > 0;
    const emptyState   = document.getElementById('analysis-empty-state');
    const contentBlock = document.getElementById('analysis-content');
    if (emptyState)   emptyState.style.display = hasResume ? 'none' : 'flex';
    if (contentBlock) contentBlock.classList.toggle('hidden', !hasResume);

    if (!hasResume) return; // Don't populate fields if no resume yet

    setEl('profile-name', d.name || '-');
    setEl('profile-email', d.email || '-');
    setEl('profile-phone', d.phone || '-');
    setEl('profile-linkedin', d.linkedin || '-');
    setEl('profile-github', d.github || '-');
    setEl('profile-education', d.education || '-');
    setEl('profile-summary', d.summary || '-');
    setEl('profile-location', d.location || '-');

    const skillsTech = document.getElementById('profile-skills-tech');
    if (skillsTech && d.skills) {
      const skillsArray = d.skills.split(',').filter(s => s.trim() !== '');
      skillsTech.innerHTML = skillsArray.map(s => `<span class="skill-tag skill-neutral">${s.trim()}</span>`).join('');
    }

    // ── Projects: show empty state if none extracted ──
    const projectsList  = document.getElementById('profile-projects-list');
    const projectsEmpty = document.getElementById('projects-empty-state');
    const hasProjects   = projectsList && projectsList.children.length > 0;
    if (projectsEmpty) projectsEmpty.style.display = hasProjects ? 'none' : 'block';
  });
}


function setEl(id, val) {
  const el = document.getElementById(id);
  if(el) el.textContent = val;
}

function updateSidebarBadges() {
  const cNotifs = DB.notifications ? DB.notifications.filter(n=>n.unread).length : 0;
  const upd = (id, count) => {
    const el = document.getElementById(id);
    if(el) {
      el.textContent = count;
      el.style.display = count > 0 ? 'inline-flex' : 'none';
    }
  };

  // HR Admin Badges
  upd('badge-admin-candidates', DB.candidates ? DB.candidates.length : 0);
  upd('badge-admin-jobs', DB.jobs ? DB.jobs.length : 0);
  upd('badge-admin-notifs', cNotifs);

  // Candidate Badges
  const score = DB.currentUser ? (DB.currentUser.ats_score || 0) : 0;
  upd('badge-cand-upload', score > 0 ? 0 : 1);
  const totalJobs = DB.jobs ? DB.jobs.length : 0;
  upd('badge-cand-jobs', totalJobs);
  upd('badge-cand-notifs', cNotifs);

  // Buttons Logic
  const btnJobs = document.getElementById('ats-btn-jobs');
  if(btnJobs) { btnJobs.innerHTML = `<i class="fas fa-briefcase"></i> View Job Matches (${totalJobs})`; }
  
  const notifDots = document.querySelectorAll('.notif-dot');
  notifDots.forEach(dot => { dot.style.display = cNotifs > 0 ? 'block' : 'none'; });
}

// ── DOMContentLoaded ──────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  Router.go('landing');
  fetchJobsFromServer();
  fetchCandidatesFromServer();
  fetchAdminStats();
  UI.renderNotifications('cand');
  UI.renderNotifications('admin');
  // Fetch and display real landing stats
  fetch('/api/auth/landing_stats').then(r => r.json()).then(d => {
    const rEl = document.getElementById('hero-stat-resumes');
    const jEl = document.getElementById('hero-stat-jobs');
    if (rEl) rEl.textContent = d.resumes_analyzed > 0 ? d.resumes_analyzed + '+' : '12+';
    if (jEl) jEl.textContent = d.jobs_matched > 0 ? d.jobs_matched + '+' : '10+';
  }).catch(() => {});
  
  // Lightweight auto-refresh every 2 min (only stats, NOT the heavy ML pipeline)
  setInterval(() => {
    if (document.hidden) return;  // Don't poll when tab is in background
    if (DB.currentUser?.role === 'hr') {
      fetchAdminStats();
      fetchCandidatesFromServer();
    }
  }, 120000);

  // Bind settings toggles
  ['email','sms','jobs','profile'].forEach(key => {
    const el = document.getElementById(`toggle-${key}`);
    if (el) el.checked = DB.settings[key === 'email' ? 'emailNotif' : key === 'sms' ? 'smsNotif' : key === 'jobs' ? 'jobAlerts' : 'profileVisible'];
  });

  // ATS score SVG animations
  animateATSRings();

  // Close modal on backdrop click
  document.querySelectorAll('.modal-backdrop').forEach(m => {
    m.addEventListener('click', e => { if (e.target === m) m.classList.remove('show'); });
  });

  // Candidate tab filter
  document.querySelectorAll('[data-tabgroup="cand-filter"]').forEach(btn => {
    btn.addEventListener('click', function() {
      switchTab(this, 'cand-filter');
      const filter = this.dataset.filter || 'All';
      UI.renderCandidatesTable(filter);
    });
  });
});

// ── Mobile Landing Menu ──────────────────────────────────────
function toggleMobileMenu() {
  const menu = document.getElementById('land-mobile-menu');
  if (!menu) return;
  menu.classList.toggle('open');
  document.body.style.overflow = menu.classList.contains('open') ? 'hidden' : '';
}

function closeMobileMenuAndScroll(sectionId) {
  toggleMobileMenu();
  setTimeout(() => {
    const el = document.getElementById(sectionId);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }, 200);
}

function animateATSRings() {
  // Animate all SVG score rings
  document.querySelectorAll('.animated-ring').forEach(ring => {
    const score = parseInt(ring.dataset.score || 78);
    const r = 54;
    const circum = 2 * Math.PI * r;
    const fill = ring.querySelector('.ring-fill');
    if (fill) {
      fill.style.strokeDasharray = circum;
      fill.style.strokeDashoffset = circum;
      setTimeout(() => {
        fill.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(.4,0,.2,1)';
        fill.style.strokeDashoffset = circum * (1 - score/100);
      }, 300);
    }
  });
}

// Global expose for inline handlers
window.Router    = Router;
window.Auth      = Auth;
window.Toast     = Toast;
window.Modal     = Modal;
window.Sidebar   = Sidebar;
window.UI        = UI;
window.Charts    = Charts;
window.switchTab = switchTab;
window.applyJob  = applyJob;
window.editJob   = editJob;
window.saveEditJob = saveEditJob;
window.deleteJob = deleteJob;
window.postJob   = postJob;
window.viewCandidate = viewCandidate;
window.viewJobRankings = viewJobRankings;
window.exportCSV = exportCSV;
window.searchCandidates = searchCandidates;
window.filterJobs = filterJobs;
window.resetFilters = resetFilters;
window.saveProfile = saveProfile;
window.changePwd = changePwd;
window.saveSettings = saveSettings;
window.markAllRead = markAllRead;
window.resumeUpload = resumeUpload;
window.handleDrop = handleDrop;
window.topbarSearch = topbarSearch;
window.updateCandidateStatus = updateCandidateStatus;
window.animateATSRings = animateATSRings;
window.fetchJobsFromServer = fetchJobsFromServer;
window.fetchCandidatesFromServer = fetchCandidatesFromServer;
window.fetchAdminStats = fetchAdminStats;
window.fetchNotificationsFromServer = fetchNotificationsFromServer;
window.fetchCandidateStats = fetchCandidateStats;
window.setEl = setEl;
window.switchSettingTab = switchSettingTab;
window.toggleDarkMode = toggleDarkMode;
window.toggleMobileMenu = toggleMobileMenu;
window.closeMobileMenuAndScroll = closeMobileMenuAndScroll;
window.viewMatchedJobs = viewMatchedJobs;
window.triggerReupload = triggerReupload;
window.fetchJobs = fetchJobs;

// ── Cluster View Renderer ─────────────────────────────────────────────────
function renderClusterView() {
  const container = document.getElementById('cluster-view-container');
  if (!container || !DB.candidates) return;

  // Group candidates by cluster label
  const groups = {};
  DB.candidates.forEach(c => {
    const label = c.cluster_label || 'Unclustered';
    if (!groups[label]) groups[label] = [];
    groups[label].push(c);
  });

  // Sort each group by ATS score desc
  Object.values(groups).forEach(g => g.sort((a, b) => b.ats - a.ats));

  const clusterColors = {
    'Python / Data Science':  '#2563eb',
    'Frontend / UI Developer':'#7c3aed',
    'DevOps / Cloud Engineer':'#059669',
    'Java / Backend Developer':'#b45309',
    'Database / Data Engineer':'#0891b2',
    'Mobile Developer':        '#db2777',
    'General / Mixed Skills':  '#6b7280',
    'Unclustered':             '#9ca3af'
  };

  container.innerHTML = Object.entries(groups).map(([label, members]) => {
    const cleanLabel = label.replace(/[\u{1F000}-\u{1FFFF}]/gu, '').trim();
    const color = Object.entries(clusterColors).find(([k]) => cleanLabel.includes(k.split('/')[0].trim()))?.[1] || '#6b7280';
    const flagged = members.filter(c => c.outlier_flag).length;

    return `
      <div class="card" style="margin-bottom:18px;border-left:4px solid ${color}">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px">
          <div style="display:flex;align-items:center;gap:10px">
            <div style="width:10px;height:10px;border-radius:50%;background:${color}"></div>
            <span style="font-weight:700;font-size:15px">${label}</span>
            <span style="background:#f1f5f9;color:#64748b;font-size:12px;padding:2px 10px;border-radius:12px">${members.length} candidates</span>
            ${flagged > 0 ? `<span style="background:#fee2e2;color:#dc2626;font-size:11px;padding:2px 8px;border-radius:12px;font-weight:600">\u26a0\ufe0f ${flagged} flagged</span>` : ''}
          </div>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:10px">
          ${members.map(c => `
            <div style="display:flex;align-items:center;gap:8px;background:${c.outlier_flag?'#fff5f5':'var(--bg-2)'};border:1px solid ${c.outlier_flag?'#fca5a5':'var(--border)'};border-radius:8px;padding:8px 12px;min-width:200px;flex:1">
              <div class="avatar avatar-sm" style="background:${UI.avatarColor(c.name)};color:#fff;flex-shrink:0">${c.name.slice(0,2).toUpperCase()}</div>
              <div style="min-width:0">
                <div style="font-weight:600;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${c.name}</div>
                <div style="font-size:11px;color:var(--text-3)">${c.job}</div>
                <div style="display:flex;align-items:center;gap:6px;margin-top:4px">
                  <span class="badge ${UI.atsBadge(c.ats)}" style="font-size:10px">${c.ats}/100</span>
                  ${c.outlier_flag ? '<span style="font-size:10px;color:#dc2626;font-weight:700">\u26a0\ufe0f</span>' : ''}
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>`;
  }).join('') || '<div style="text-align:center;padding:40px;color:var(--text-3)">No candidates to cluster yet.</div>';
}
window.renderClusterView = renderClusterView;
// ── Change Profile Photo ──────────────────────────────────────────────────────
function applyAvatarPhoto(portal, dataUrl) {
  const sel = portal === 'cand' ? '.cand-avatar' : '.admin-avatar';
  document.querySelectorAll(sel).forEach(el => {
    el.textContent              = '';
    el.style.backgroundImage    = `url('${dataUrl}')`;
    el.style.backgroundSize     = 'cover';
    el.style.backgroundPosition = 'center';
    el.style.color              = 'transparent';
  });
}

function changeProfilePhoto(input, portal) {
  if (!input.files || !input.files[0]) return;
  const file = input.files[0];
  if (!file.type.startsWith('image/')) {
    Toast.show('Please select a valid image file.', 'error');
    return;
  }
  const reader = new FileReader();
  reader.onload = function(e) {
    const dataUrl = e.target.result;
    applyAvatarPhoto(portal, dataUrl);
    try { localStorage.setItem(`hireai_${portal}_photo`, dataUrl); } catch(err) {}
    Toast.show('Profile photo updated! ✓', 'success');
  };
  reader.readAsDataURL(file);
}
window.changeProfilePhoto = changeProfilePhoto;
