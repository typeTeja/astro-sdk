# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of AstroSDK seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Where to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **security@yourdomain.com** *(replace with actual email)*

### What to Include

Please include the following information in your report:

- Type of vulnerability (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the vulnerability
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- **Initial Response**: Within 48 hours of report submission
- **Status Update**: Within 7 days with assessment and planned fix timeline
- **Resolution**: Security patches released as soon as possible, typically within 30 days

### Disclosure Policy

- We will acknowledge receipt of your vulnerability report
- We will confirm the vulnerability and determine its impact
- We will release a fix as part of a security update
- We will publicly disclose the vulnerability after a fix is available

### Safe Harbor

We support safe harbor for security researchers who:

- Make a good faith effort to avoid privacy violations, destruction of data, and interruption or degradation of our services
- Only interact with accounts you own or with explicit permission of the account holder
- Do not exploit a security issue you discover for any reason (including demonstrating additional risk)
- Report the vulnerability to us before disclosing it publicly

## Security Best Practices for Users

### Input Validation

While AstroSDK validates planetary bodies and time inputs, users should:

- Validate latitude/longitude ranges before passing to the SDK
- Sanitize any user-provided input before calculation
- Implement rate limiting for calculation-heavy operations

### Dependency Management

- Keep pyswisseph updated to the latest stable version
- Regularly update Python to receive security patches
- Monitor security advisories for dependencies

### Thread Safety

- AstroSDK is thread-safe, but ensure your application properly handles concurrent access
- Use appropriate locking mechanisms in your application layer

### Financial Applications

If using AstroSDK in financial applications:

- **Never** use astronomical data as the sole basis for financial decisions
- Implement proper risk management and compliance checks
- Ensure regulatory compliance in your jurisdiction
- Add appropriate disclaimers to end users

### Data Privacy

- AstroSDK does not collect, store, or transmit any user data
- Birth data and calculation results remain in your application's memory
- Implement appropriate data protection measures in your application

## Known Limitations

### Not Security Vulnerabilities

The following are known limitations by design and are NOT security vulnerabilities:

1. **Global State**: Swiss Ephemeris uses global mutable state (protected by RLock)
2. **File System Access**: Requires read access to ephemeris data files
3. **No Sandboxing**: Calculations run in the same process as your application
4. **No Rate Limiting**: SDK does not implement rate limiting (implement in your application)

## Security Considerations

### Determinism vs. Security

AstroSDK prioritizes determinism over security-through-obscurity:

- Calculations are reproducible (same input → same output)
- No randomization or obfuscation
- All algorithms are transparent and auditable

This is intentional for research and compliance purposes.

### No Network Access

AstroSDK does not:

- Make network requests
- Connect to external services
- Download ephemeris data
- Send telemetry or analytics

All calculations are performed locally.

## Acknowledgments

We appreciate the security research community's efforts in responsibly disclosing vulnerabilities. Security researchers who report valid vulnerabilities will be acknowledged in our security advisories (unless they prefer to remain anonymous).

---

**Last Updated**: February 15, 2026
