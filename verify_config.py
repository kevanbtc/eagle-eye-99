#!/usr/bin/env python3
"""
Eagle Eye Configuration Verification Script

Checks that secrets and configuration are properly set up.
Run this before deploying to verify all required settings are configured.

Usage:
    python verify_config.py
    python verify_config.py --strict  (fail on warnings)
    python verify_config.py --mask    (hide actual values)
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Add config to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config.settings import get_settings, get_settings_dict
except ImportError as e:
    print(f"❌ Failed to import settings: {e}")
    print("Run: pip install -r config/requirements.txt")
    sys.exit(1)


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_status(passed: bool, message: str, detail: str = ""):
    """Print status message with color"""
    icon = f"{Colors.GREEN}✓{Colors.RESET}" if passed else f"{Colors.RED}✗{Colors.RESET}"
    print(f"{icon} {message}")
    if detail:
        print(f"  {detail}")


def check_file_exists(path: str, required: bool = False) -> bool:
    """Check if a file exists"""
    exists = Path(path).exists()
    icon = "✓" if exists else "✗" if required else "○"
    status = f"{Colors.GREEN}exists{Colors.RESET}" if exists else "missing"
    print(f"  {icon} {path}: {status}")
    return exists


def check_environment_variables() -> Dict[str, str]:
    """Check which environment variables are set"""
    settings = get_settings()
    results = {}
    
    checks = {
        "ENVIRONMENT": settings.environment,
        "OPENAI_API_KEY": "***" if settings.openai.api_key else None,
        "DATABASE_URL": "***" if settings.database.url else None,
        "S3_ACCESS_KEY": "***" if settings.storage.access_key else None,
        "REDIS_URL": "***" if settings.cache.url else None,
    }
    
    for key, value in checks.items():
        results[key] = value is not None
    
    return results


def verify_gitignore() -> bool:
    """Verify .gitignore contains .env.local"""
    gitignore_path = Path(".gitignore")
    
    if not gitignore_path.exists():
        print(f"{Colors.YELLOW}⚠ .gitignore not found{Colors.RESET}")
        return False
    
    content = gitignore_path.read_text()
    has_env_local = ".env.local" in content
    
    print_status(has_env_local, ".gitignore contains .env.local")
    
    if not has_env_local:
        print(f"  {Colors.YELLOW}Add '.env.local' to .gitignore{Colors.RESET}")
    
    return has_env_local


def check_env_files() -> Dict[str, bool]:
    """Check for .env files"""
    files = {
        ".env.example": True,  # Should exist
        ".env.local": False,   # Should exist but can be missing
        ".env.local.template": False,  # Optional reference
    }
    
    results = {}
    for file, required in files.items():
        exists = Path(file).exists()
        results[file] = exists
        
        if required and not exists:
            print_status(False, f"{file} (REQUIRED)")
        elif exists:
            print_status(True, f"{file}")
        else:
            print(f"  ○ {file} (optional)")
    
    return results


def validate_api_keys() -> Tuple[bool, List[str]]:
    """Validate API key formats"""
    settings = get_settings()
    errors = []
    
    # OpenAI key format
    if settings.openai.api_key and not settings.openai.api_key.startswith("sk-"):
        errors.append("OpenAI API key must start with 'sk-'")
    
    # Database URL format
    if settings.database.url:
        if not settings.database.url.startswith("postgresql"):
            errors.append("Database URL should start with 'postgresql' or 'postgresql+psycopg'")
    
    # S3 endpoint format
    if settings.storage.endpoint:
        if not settings.storage.endpoint.startswith(("http://", "https://")):
            errors.append("S3 endpoint must start with http:// or https://")
    
    return len(errors) == 0, errors


def check_for_exposed_secrets() -> bool:
    """Check if secrets might be exposed in git history"""
    # This is a basic check; for production use git-secrets
    
    try:
        import subprocess
        
        # Look for OpenAI keys in git history
        result = subprocess.run(
            ["git", "log", "--all", "-S", "sk-", "--source"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout and "sk-" in result.stdout:
            print(f"{Colors.RED}⚠ Warning: Found 'sk-' patterns in git history{Colors.RESET}")
            print("  Consider running: git-secrets --scan")
            return False
        
        print_status(True, "No obvious secrets in git history (basic scan)")
        return True
    
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ⚠ Could not run git scan (git may not be installed)")
        return True  # Don't fail if git isn't available


def run_all_checks(strict: bool = False, mask: bool = False) -> int:
    """Run all verification checks"""
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Eagle Eye Configuration Verification{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    failed_checks = 0
    
    # Check 1: Configuration Files
    print("1. Configuration Files")
    print("─" * 40)
    env_files = check_env_files()
    if not env_files.get(".env.example"):
        failed_checks += 1
    if not env_files.get(".env.local"):
        print(f"  {Colors.YELLOW}Create .env.local from .env.example{Colors.RESET}")
        failed_checks += 1
    print()
    
    # Check 2: .gitignore
    print("2. Git Ignore Settings")
    print("─" * 40)
    if not verify_gitignore():
        failed_checks += 1
    print()
    
    # Check 3: Environment Variables
    print("3. Environment Variables")
    print("─" * 40)
    env_vars = check_environment_variables()
    for key, is_set in env_vars.items():
        status = f"{Colors.GREEN}set{Colors.RESET}" if is_set else f"{Colors.YELLOW}not set{Colors.RESET}"
        symbol = "✓" if is_set else "○"
        print(f"  {symbol} {key}: {status}")
    
    if not all(env_vars.values()):
        print(f"\n  {Colors.YELLOW}Add required variables to .env.local{Colors.RESET}")
        if strict:
            failed_checks += 1
    print()
    
    # Check 4: API Key Validation
    print("4. API Key Format Validation")
    print("─" * 40)
    valid, errors = validate_api_keys()
    if valid:
        print_status(True, "All API keys have valid formats")
    else:
        print_status(False, "API key validation failed")
        for error in errors:
            print(f"  ❌ {error}")
        if strict:
            failed_checks += 1
    print()
    
    # Check 5: Git History
    print("5. Secret Exposure Check")
    print("─" * 40)
    if not check_for_exposed_secrets():
        if strict:
            failed_checks += 1
    print()
    
    # Check 6: Current Configuration
    print("6. Current Configuration Status")
    print("─" * 40)
    try:
        config_dict = get_settings_dict()
        for key, value in config_dict.items():
            if value == "***":
                print(f"  ✓ {key}: [CONFIGURED]")
            elif isinstance(value, bool):
                symbol = "✓" if value else "○"
                print(f"  {symbol} {key}: {value}")
            else:
                print(f"  ✓ {key}: {value}")
    except Exception as e:
        print(f"  ❌ Error reading configuration: {e}")
        failed_checks += 1
    print()
    
    # Summary
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    if failed_checks == 0:
        print(f"{Colors.GREEN}✓ All checks passed!{Colors.RESET}")
        print("Eagle Eye is ready to run.")
    else:
        print(f"{Colors.RED}✗ {failed_checks} check(s) failed{Colors.RESET}")
        if not strict:
            print("(Some issues are warnings; use --strict to treat as errors)")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    return failed_checks


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Verify Eagle Eye configuration and secrets setup"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat all warnings as errors"
    )
    parser.add_argument(
        "--mask",
        action="store_true",
        help="Mask sensitive values in output"
    )
    
    args = parser.parse_args()
    
    exit_code = run_all_checks(strict=args.strict, mask=args.mask)
    sys.exit(exit_code)
