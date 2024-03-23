import files
from pathlib import Path
import asyncio
import tornado
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("search.html", title="Project Diablo2 Armory")

class CharSaveHandler(tornado.web.RequestHandler):
    def get(self, char_name):
        # Read character
        char_save_path = Path(__file__).parent.joinpath('test/char/'+char_name.lower())
        print(char_save_path)
        try:
            d2s_file = files.D2SFile(char_save_path)
        except Exception as error:
            print(error)
            self.write("%s does exist" % char_name)
            return
        # Read inventory
        stash_save_path = Path(__file__).parent.joinpath('test/save/'+char_name+'.d2x')
        print(stash_save_path)
        try:
            char_equipped = set()
            inventory = []
            splitter = files.D2XFileSplitter(stash_save_path, True).stash
            for item in  next(iter(splitter.values())):
                if item.location_id != 1:
                    inventory.append(item)
                    continue
                if item.equipped_id in char_equipped:
                    continue
                inventory.append(item)
                char_equipped.add(item.equipped_id)
        except Exception as error:
            inventory = []
            print(error)
        self.render("char_save_tmpl.html", title="Project Diablo2 Armory", char_save=d2s_file.to_dict(), inventory=inventory)

class CharStashHandler(tornado.web.RequestHandler):
    def get(self, char_name):
        save_path = Path(__file__).parent.joinpath('test/save/'+char_name+'.d2x')
        print(save_path)
        try:
            stash = files.D2XFileSplitter(save_path, False)
        except:
            stash = {}
        self.render("char_stash_tmpl.html", title="Project Diablo2 Armory", stash=stash.stash)

def make_app():
    settings = {
      "static_path": os.path.join(os.path.dirname(__file__), "static"),
      "static_url_prefix": "/static/",
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/char/(.*?)", CharSaveHandler),
        (r"/api/stash/(.*?)", CharStashHandler),
        (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler,
          dict(path=settings['static_path'])),
    ],
    debug=True,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    **settings,)

async def main():
    app = make_app()
    app.listen(8080)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
