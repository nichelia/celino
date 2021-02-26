from app._version import __version__
from app.settings import settings

LOGO = r'''
    ___       ___       ___       ___       ___       ___   
   /\  \     /\  \     /\__\     /\  \     /\__\     /\  \  
  /::\  \   /::\  \   /:/  /    _\:\  \   /:| _|_   /::\  \ 
 /:/\:\__\ /::\:\__\ /:/__/    /\/::\__\ /::|/\__\ /:/\:\__\
 \:\ \/__/ \:\:\/  / \:\  \    \::/\/__/ \/|::/  / \:\/:/  /
  \:\__\    \:\/  /   \:\__\    \:\__\     |:/  /   \::/  / 
   \/__/     \/__/     \/__/     \/__/     \/__/     \/__/  
'''


def render():
  lines = LOGO.splitlines()[1:]
  lines.append("")
  tag = f"{settings.PROJECT_NAME} v{__version__}"
  prefix = len(lines[0]) - len(tag)
  lines.append(f"{' '*prefix}{tag}")
  return '\n'.join(lines)
