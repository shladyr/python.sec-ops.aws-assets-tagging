# Security Policy

## Supported Versions

We take security seriously and are committed to ensuring that our project remains secure. The following versions of the AWS Tagging Tool are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark:  |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please follow these steps:

1. **Do Not Disclose Publicly:** Please do not publicly disclose the vulnerability until we have had a chance to address it.

2. **Contact Us:**
   - Send an email to [security@example.com](mailto:security@example.com) with the subject line "Security Vulnerability Report".
   - Include a detailed description of the vulnerability, including steps to reproduce it and any potential impact.
   - Optionally, you can encrypt your report using [PGP keys](https://example.com/pgp-key) to ensure confidentiality.

3. **Acknowledgment:**
   - We will acknowledge your report within 48 hours and provide an estimated timeline for the fix.

4. **Mitigation:**
   - We will work to validate the issue, and if necessary, we will develop and release a patch or workaround.

5. **Credit:**
   - With your permission, we will publicly acknowledge your contribution to improving the security of this project.

## Security Best Practices

This project follows best practices to ensure security compliance, including:

- **Configuration Management:** Sensitive information is managed using configuration files that are not stored in the source code repository.
- **Parameterization:** Avoiding hard-coded secrets and using environment variables for sensitive data.
- **Logging:** Logs are managed carefully to avoid logging sensitive information.
- **Error Handling:** Proper error handling is implemented to ensure that errors are managed without leaking sensitive information.
- **AWS IAM Policies:** The project uses the principle of least privilege by configuring AWS IAM roles and policies that provide only the necessary permissions.
- **Data Encryption:** All data stored in DynamoDB and transferred between services is encrypted.
- **Code Quality:** We follow PEP 8 compliance, use type annotations, and conduct regular code reviews to identify potential security issues.

## Dependencies

This project uses dependencies from third-party libraries, which are monitored and regularly updated to minimize security risks. A full list of dependencies is available in `requirements.txt`.

## Security Contact

If you have any questions about security, you can reach out to us at [security@example.com](mailto:security@example.com).

## Additional Resources

- [AWS Security Best Practices](https://aws.amazon.com/whitepapers/security/)
- [SOC-2 Compliance Information](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/socforserviceorganizations.html)

