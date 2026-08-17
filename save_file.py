PARENT = Path(__file__).parent.resolve()
SAVEFILE = PARENT / 'Messages.json'
if not SAVEFILE.exists():
    with open(SAVEFILE , 'w') as f:
        json.dump({},f)
