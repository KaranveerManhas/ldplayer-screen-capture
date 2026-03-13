import subprocess
import logging

logger = logging.getLogger("Command Runner")

def run_cmd(cmd, path):
    
    try:
        result = subprocess.run(
            cmd, cwd=path,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        logger.error("Command failed: %s", e)
        return None
    
    if result.stdout.strip():
        logger.debug("OUT: %s", result.stdout.strip())
    if result.stderr.strip():
        logger.debug("ERROR: %s", result.stderr.strip())
        
    return result