import traceback
try:
    import services
    print("SERVICES IMPORT OK")
    if services.advanced_pipeline:
        print("PIPELINE IS INITIALIZED")
    else:
        print("PIPELINE IS NONE")
except Exception as e:
    traceback.print_exc()
