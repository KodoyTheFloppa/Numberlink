import dialogs
import app

def main():
    def on_generate(rows, cols):
        numberlink_app = app.NumberlinkApp(rows, cols)
    dialogs.GridSizeDialog(on_generate)

if __name__ == "__main__":
    main()
