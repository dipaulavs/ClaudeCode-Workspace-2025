# Product Designer - Examples

## Example 1: Landing Page Hero Section

### User Request
"Design a modern hero section for my SaaS product that helps developers monitor APIs."

### Design Output

```tsx
export default function Hero() {
  return (
    <div className="relative bg-white">
      {/* Container */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28">

        {/* Grid: Text left, Image right */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

          {/* Left: Content */}
          <div className="space-y-8">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-50 rounded-full">
              <span className="w-2 h-2 bg-indigo-600 rounded-full animate-pulse"></span>
              <span className="text-sm font-medium text-indigo-900">
                Now monitoring 10M+ API calls daily
              </span>
            </div>

            {/* Headline */}
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
              Know when your API breaks
              <span className="text-indigo-600"> before</span> your users do
            </h1>

            {/* Subheadline */}
            <p className="text-xl text-gray-600 leading-relaxed max-w-xl">
              Real-time API monitoring with instant alerts. Get notified in Slack, Discord, or email when things go wrong.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <button className="
                px-6 py-3
                bg-indigo-600 text-white font-semibold rounded-lg
                hover:bg-indigo-700
                focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
                transition-colors duration-150
                shadow-sm hover:shadow-md
              ">
                Start monitoring free
              </button>

              <button className="
                px-6 py-3
                bg-white text-gray-700 font-semibold rounded-lg border-2 border-gray-300
                hover:border-gray-400 hover:bg-gray-50
                focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2
                transition-colors duration-150
              ">
                View live demo
              </button>
            </div>

            {/* Social Proof */}
            <div className="flex items-center gap-6 pt-4">
              <div className="flex -space-x-2">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="w-10 h-10 rounded-full bg-gray-200 border-2 border-white"
                  />
                ))}
              </div>
              <div className="text-sm text-gray-600">
                <span className="font-semibold text-gray-900">2,000+ developers</span> trust us with their APIs
              </div>
            </div>
          </div>

          {/* Right: Visual */}
          <div className="relative">
            {/* Dashboard mockup */}
            <div className="bg-white rounded-xl shadow-2xl border border-gray-200 p-6">
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
                <span className="text-xs text-gray-500">api-monitor.com</span>
              </div>

              {/* Status indicator */}
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="font-medium text-gray-900">All systems operational</span>
                  </div>
                  <span className="text-sm text-gray-600">99.9% uptime</span>
                </div>

                {/* Metrics */}
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { label: 'Response', value: '124ms' },
                    { label: 'Success', value: '99.8%' },
                    { label: 'Errors', value: '12' }
                  ].map((metric) => (
                    <div key={metric.label} className="p-4 bg-gray-50 rounded-lg">
                      <div className="text-xs text-gray-500 mb-1">{metric.label}</div>
                      <div className="text-xl font-bold text-gray-900">{metric.value}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Floating alert badge */}
            <div className="
              absolute -bottom-4 -left-4
              bg-white rounded-lg shadow-xl border border-gray-200 p-4
              animate-bounce
            ">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                  <span className="text-red-600 font-bold">!</span>
                </div>
                <div>
                  <div className="text-sm font-semibold text-gray-900">API Error Detected</div>
                  <div className="text-xs text-gray-500">2 seconds ago</div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
```

### Design Rationale

**Color Choice:**
- Indigo accent (trustworthy, technical)
- Neutral grays for readability
- Green/red for status (universal signals)

**Typography:**
- Large headline (60px desktop) for impact
- Clear hierarchy (headline → subheadline → CTA)
- Limited to 3 font sizes (5xl, xl, sm)

**Layout:**
- Max-width 1152px (comfortable landing page width)
- Two-column on desktop, stacks on mobile
- Generous spacing (py-20 on mobile, py-28 on desktop)

**Interactive Elements:**
- Primary CTA (solid button) vs. Secondary (outline)
- Hover states on both buttons
- Animated pulse on status indicators (draws attention)

---

## Example 2: Dashboard Card Grid

### User Request
"Design a dashboard showing project metrics in cards."

### Design Output

```tsx
export default function MetricsDashboard() {
  const metrics = [
    {
      id: 1,
      label: 'Total Revenue',
      value: '$124,450',
      change: '+12.5%',
      trend: 'up',
      icon: '💰'
    },
    {
      id: 2,
      label: 'Active Users',
      value: '8,432',
      change: '+5.2%',
      trend: 'up',
      icon: '👥'
    },
    {
      id: 3,
      label: 'Conversion Rate',
      value: '3.24%',
      change: '-0.3%',
      trend: 'down',
      icon: '📈'
    },
    {
      id: 4,
      label: 'Avg Session',
      value: '4m 32s',
      change: '+1.1%',
      trend: 'up',
      icon: '⏱️'
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Container */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Overview of your key metrics</p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {metrics.map((metric) => (
            <MetricCard key={metric.id} metric={metric} />
          ))}
        </div>

        {/* Chart Section */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900">Revenue Trend</h2>
            <select className="
              px-3 py-1.5
              border border-gray-300 rounded-lg
              text-sm text-gray-700
              focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
            ">
              <option>Last 7 days</option>
              <option>Last 30 days</option>
              <option>Last 90 days</option>
            </select>
          </div>

          {/* Placeholder for chart */}
          <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <span className="text-gray-400">Chart goes here</span>
          </div>
        </div>

      </div>
    </div>
  );
}

function MetricCard({ metric }) {
  return (
    <div className="
      bg-white rounded-lg border border-gray-200 p-6
      hover:shadow-md transition-shadow duration-200
    ">
      {/* Top: Icon and Trend */}
      <div className="flex items-start justify-between mb-4">
        <div className="text-3xl">{metric.icon}</div>
        <div className={`
          flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium
          ${metric.trend === 'up'
            ? 'bg-green-100 text-green-700'
            : 'bg-red-100 text-red-700'
          }
        `}>
          <span>{metric.trend === 'up' ? '↑' : '↓'}</span>
          <span>{metric.change}</span>
        </div>
      </div>

      {/* Bottom: Label and Value */}
      <div className="space-y-1">
        <p className="text-sm text-gray-600">{metric.label}</p>
        <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
      </div>
    </div>
  );
}
```

### Design Rationale

**Layout:**
- Responsive grid: 1 col mobile, 2 tablet, 4 desktop
- Consistent gap (24px) between cards
- Max-width container (1280px) prevents excessive width

**Card Design:**
- White background (stands out from gray page background)
- Subtle border (not shadow) for clean look
- Shadow on hover only (interactive feedback)
- Generous padding (24px) for breathing room

**Visual Hierarchy:**
- Large value (24px bold) is focal point
- Label is secondary (14px gray)
- Trend badge uses color (green/red) for quick scanning

**Spacing:**
- 8px grid throughout (gaps of 4, 16, 24px)
- Consistent internal card spacing (24px padding, 16px between elements)

---

## Example 3: Form with Validation States

### User Request
"Design a sign-up form with proper validation states."

### Design Output

```tsx
'use client';

import { useState } from 'react';

export default function SignUpForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const validatePassword = (password) => {
    return password.length >= 8;
  };

  const handleBlur = (field) => {
    setTouched({ ...touched, [field]: true });

    const newErrors = { ...errors };

    if (field === 'email') {
      if (!email) {
        newErrors.email = 'Email is required';
      } else if (!validateEmail(email)) {
        newErrors.email = 'Please enter a valid email';
      } else {
        delete newErrors.email;
      }
    }

    if (field === 'password') {
      if (!password) {
        newErrors.password = 'Password is required';
      } else if (!validatePassword(password)) {
        newErrors.password = 'Password must be at least 8 characters';
      } else {
        delete newErrors.password;
      }
    }

    setErrors(newErrors);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Create your account
          </h1>
          <p className="text-gray-600">
            Start your 14-day free trial. No credit card required.
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
          <form className="space-y-6">

            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-900 mb-2">
                Email address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onBlur={() => handleBlur('email')}
                className={`
                  w-full px-4 py-2.5 rounded-lg
                  border transition-colors duration-150
                  placeholder:text-gray-400
                  focus:outline-none focus:ring-2
                  ${
                    errors.email && touched.email
                      ? 'border-red-500 focus:border-red-500 focus:ring-red-500 focus:ring-opacity-20'
                      : email && !errors.email && touched.email
                      ? 'border-green-500 focus:border-green-500 focus:ring-green-500 focus:ring-opacity-20'
                      : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 focus:ring-opacity-20'
                  }
                `}
                placeholder="you@example.com"
              />

              {/* Error message */}
              {errors.email && touched.email && (
                <div className="flex items-center gap-1 mt-2 text-sm text-red-600">
                  <span>⚠️</span>
                  <span>{errors.email}</span>
                </div>
              )}

              {/* Success indicator */}
              {!errors.email && email && touched.email && (
                <div className="flex items-center gap-1 mt-2 text-sm text-green-600">
                  <span>✓</span>
                  <span>Looks good!</span>
                </div>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-900 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onBlur={() => handleBlur('password')}
                className={`
                  w-full px-4 py-2.5 rounded-lg
                  border transition-colors duration-150
                  placeholder:text-gray-400
                  focus:outline-none focus:ring-2
                  ${
                    errors.password && touched.password
                      ? 'border-red-500 focus:border-red-500 focus:ring-red-500 focus:ring-opacity-20'
                      : password && !errors.password && touched.password
                      ? 'border-green-500 focus:border-green-500 focus:ring-green-500 focus:ring-opacity-20'
                      : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 focus:ring-opacity-20'
                  }
                `}
                placeholder="••••••••"
              />

              {errors.password && touched.password && (
                <div className="flex items-center gap-1 mt-2 text-sm text-red-600">
                  <span>⚠️</span>
                  <span>{errors.password}</span>
                </div>
              )}

              {!errors.password && password && touched.password && (
                <div className="flex items-center gap-1 mt-2 text-sm text-green-600">
                  <span>✓</span>
                  <span>Strong password</span>
                </div>
              )}
            </div>

            {/* Terms checkbox */}
            <div className="flex items-start gap-3">
              <input
                type="checkbox"
                id="terms"
                className="
                  w-4 h-4 mt-0.5
                  border-gray-300 rounded
                  text-indigo-600 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-20
                "
              />
              <label htmlFor="terms" className="text-sm text-gray-600">
                I agree to the{' '}
                <a href="#" className="text-indigo-600 hover:text-indigo-700 font-medium">
                  Terms of Service
                </a>{' '}
                and{' '}
                <a href="#" className="text-indigo-600 hover:text-indigo-700 font-medium">
                  Privacy Policy
                </a>
              </label>
            </div>

            {/* Submit button */}
            <button
              type="submit"
              className="
                w-full px-4 py-3
                bg-indigo-600 text-white font-semibold rounded-lg
                hover:bg-indigo-700
                focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
                disabled:bg-gray-300 disabled:cursor-not-allowed
                transition-colors duration-150
                shadow-sm hover:shadow-md
              "
            >
              Create account
            </button>

          </form>

          {/* Footer */}
          <div className="mt-6 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <a href="#" className="text-indigo-600 hover:text-indigo-700 font-medium">
              Sign in
            </a>
          </div>
        </div>

      </div>
    </div>
  );
}
```

### Design Rationale

**Validation States:**
- **Default:** Gray border
- **Error:** Red border + red ring + error message
- **Success:** Green border + green ring + success message
- **Focus:** Ring opacity 20% (subtle, not distracting)

**User Experience:**
- Validate on blur (not on every keystroke)
- Show errors only after field is touched
- Instant success feedback for positive reinforcement

**Accessibility:**
- Labels properly associated with inputs (htmlFor)
- Error messages have icons for color-blind users
- Focus states clearly visible (ring)
- Color not the only indicator (text + icons)

**Spacing:**
- 24px between form fields (comfortable)
- 8px between label and input (tight grouping)
- Max-width 448px (optimal form width)

---

**More Examples:**
- Modal dialogs with backdrop
- Data tables with sorting
- Navigation menus (mobile + desktop)
- Empty states with illustrations
- Loading skeletons

**Related:** See `TROUBLESHOOTING.md` for common design problems.
