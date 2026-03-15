import traceback

try:
    import advanced_bill_pipeline
    print("Import successful")
except Exception as e:
    with open("error_log.txt", "w", encoding="utf-8") as f:
        traceback.print_exc(file=f)
    print("Import failed. Check error_log.txt")
