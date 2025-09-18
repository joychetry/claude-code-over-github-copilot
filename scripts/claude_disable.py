#!/usr/bin/env python3
"""
Script to disable Claude Code proxy configuration.
Usage: claude_disable.py
"""
import json
import sys
from pathlib import Path

def main():
    claude_dir = Path.home() / '.claude'
    settings_file = claude_dir / 'settings.json'

    if not settings_file.exists():
        print('✅ No settings file found - using Claude Code defaults')
        return

    try:
        # Load current settings
        with open(settings_file, 'r') as f:
            settings = json.load(f)

        # Remove proxy configuration
        if 'env' in settings:
            del settings['env']

        # Restore model to opusplan if it was claude-sonnet-4
        if 'model' in settings and settings['model'] == 'claude-sonnet-4':
            settings['model'] = 'opusplan'

        # Save updated settings
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)

        print('✅ Removed proxy configuration while preserving other settings')

    except Exception as e:
        print(f'❌ Error updating settings: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()