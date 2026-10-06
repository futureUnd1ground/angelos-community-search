"""Execute the native catalog provider with deterministic service/process doubles."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]

class SearchTests(unittest.TestCase):
    def test_catalog_search(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            def write(name,content):
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
            source=(ROOT/'Launcher.qml').read_text().replace('id: root','id: root\n    property alias testReader: reader',1)
            write('Launcher.qml',source)
            write('imports/Quickshell/Io/qmldir','module Quickshell.Io\nProcess 1.0 Process.qml\nStdioCollector 1.0 StdioCollector.qml\n')
            write('imports/Quickshell/Io/Process.qml','import QtQuick\nItem { property var command: []; property bool running: false; property QtObject stdout; property QtObject stderr; signal exited(int code) }')
            write('imports/Quickshell/Io/StdioCollector.qml','import QtQuick\nQtObject { property string text: "" }')
            write('imports/qs/services/qmldir','module qs.services\nsingleton Plugins 1.0 Plugins.qml\nsingleton Shell 1.0 Shell.qml\n')
            write('imports/qs/services/Plugins.qml','pragma Singleton\nimport QtQuick\nQtObject { function byId(id) { return id==="dog-walk" ? {version:"1.5.0"} : null; } function context(p) { return null; } }')
            write('imports/qs/services/Shell.qml','pragma Singleton\nimport QtQuick\nQtObject { property string page: ""; property string sub: ""; function openSettings(p,s) {page=p;sub=s||"";} }')
            write('tst_search.qml','''import QtQuick
import QtTest
import qs.services
TestCase {
 name: "CommunitySearch"
 Launcher {id: provider}
 function init() {
   provider.plugin={dir:"/search"}; provider.testReader.running=false; provider.status="ready";
   provider.entries=[{id:"dog-walk",name:"Dog Walk",description:"Питомец",author:"alice",version:"1.5.0",tags:["pets"],status:"approved"}];
 }
 function test_catalog_queries_and_card() {
   compare(provider.query("dog",false).length,1);
   compare(provider.query("питомец",false).length,1);
   compare(provider.query("alice",false).length,1);
   compare(provider.query("plugins",false).length,1);
   verify(provider.query("dog",false)[0].subtitle.includes("Установлен v1.5.0"));
   compare(provider.query("unknown",false).length,0);
   compare(provider.query("",false).length,0);
   verify(!provider.activate("plugin:dog-walk"));
   compare(Shell.page,"plugin:community-store");compare(Shell.sub,"dog-walk");
 }
 function test_publish_shortcut() {
   compare(provider.query("publish",true)[0].id,"publish");
   compare(provider.query("опубликовать zip",false)[0].id,"publish");
   verify(!provider.activate("publish"));compare(Shell.sub,"publish");
 }
 function test_first_search_fetches_once_and_filters_pending() {
   provider.status="idle";
   provider.query("dog",false);verify(provider.testReader.running);
   compare(provider.testReader.command[2],"https://raw.githubusercontent.com/futureUnd1ground/angelos-community-registry/main/plugins.json");
   provider.testReader.stdout.text=JSON.stringify({plugins:[{id:"approved",status:"approved"},{id:"pending",status:"pending"}]});
   provider.testReader.running=false;provider.testReader.exited(0);
   compare(provider.entries.length,1);compare(provider.status,"ready");
 }
 function test_error_and_retry() {
   provider.testReader.stderr.text="Network unavailable";
   provider.testReader.exited(1);compare(provider.status,"error");
   compare(provider.query("",true)[1].id,"retry");
   verify(provider.activate("retry"));verify(provider.testReader.running);
 }
}''')
            r=subprocess.run(['/usr/lib/qt6/bin/qmltestrunner','-input',tmp,'-import',str(root/'imports')],capture_output=True,text=True,env={**os.environ,'QT_QPA_PLATFORM':'offscreen','QT_QUICK_BACKEND':'software'},timeout=30)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
if __name__=='__main__':unittest.main()
