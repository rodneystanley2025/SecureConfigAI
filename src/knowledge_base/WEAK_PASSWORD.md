# Weak Password

**ID:** `WEAK_PASSWORD`
**Severity:** HIGH

## Description

A weak, default, or common password was found. A significant vulnerability because it lacks the necessary characteristics to withstand modern hacking techniques, making it easy for attackers to guess or crack through methods like brute force, dictionary attacks, or credential stuffing. Such passwords are often short, lack complexity, contain common words or personal information, follow predictable patterns, or are reused across multiple accounts, all of which drastically reduce their security and increase the risk of unauthorized access.

## Remediation

All passwords should be strong, unique, and rotated regularly.

To remediate this issue, you should:

1.  **Replace Weak Passwords:** Replace all weak and default passwords with strong, randomly generated passwords. A strong password should be at least 16 characters long and contain a mix of uppercase letters, lowercase letters, numbers, and symbols.
2.  **Use a Password Manager:** Use a password manager to generate and store strong, unique passwords for all your services.
3.  **Implement Password Policies:** Enforce strong password policies for all users and services, including minimum length, complexity, and password history requirements.
4.  **Enable Multi-Factor Authentication (MFA):** Where possible, enable MFA for all accounts to provide an additional layer of security.
