export default function Logo({ size = 32 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="QA Engine Logo">
      <defs>
        <linearGradient id="lg" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#3b82f6" />
          <stop offset="100%" stopColor="#00cfff" />
        </linearGradient>
      </defs>
      <rect width="40" height="40" rx="10" fill="rgba(26,86,255,0.12)" stroke="url(#lg)" strokeWidth="1.2" />
      {/* Shield outline */}
      <path d="M20 8 L30 12 L30 20 C30 26 20 32 20 32 C20 32 10 26 10 20 L10 12 Z" stroke="url(#lg)" strokeWidth="1.4" fill="none" strokeLinejoin="round" />
      {/* Check */}
      <path d="M15.5 20 L18.5 23 L24.5 17" stroke="#00cfff" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}
