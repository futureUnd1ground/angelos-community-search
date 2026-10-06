import QtQuick
import Quickshell.Io
import qs.services

Item {
    id: root
    visible: false
    width: 0
    height: 0
    property var plugin
    property string pluginId
    readonly property string prefix: "market"
    readonly property bool global: true
    property var entries: []
    property string status: "idle"
    property string error: ""
    signal changed

    function fetch() {
        if (!plugin || reader.running)
            return
        status = "loading"
        error = ""
        const localStore = Plugins.byId("community-store")
        const store = localStore ? Plugins.context(localStore) : null
        const url = store ? store.get("registryUrl", "https://raw.githubusercontent.com/futureUnd1ground/angelos-community-registry/main/plugins.json") : "https://raw.githubusercontent.com/futureUnd1ground/angelos-community-registry/main/plugins.json"
        reader.command = ["python3", plugin.dir + "/scripts/catalog.py", url]
        reader.running = true
        changed()
    }
    function query(text, prefixed) {
        const q = String(text || "").trim().toLowerCase()
        if (!prefixed && q.length < 2)
            return []
        if (status === "idle")
            fetch()
        const out = []
        if (prefixed && !q || ["publish", "опубликовать", "выложить", "публикация", "zip"].some(word => q.includes(word)))
            out.push({id: "publish", title: "Опубликовать ZIP в Market", subtitle: "Выбрать ZIP → отправить на проверку одной кнопкой", icon: "cloud", score: 180})
        if (status === "loading") {
            if (prefixed)
                out.push({id: "loading", title: "Загружаю каталог Community Store…", subtitle: "", icon: "refresh", score: 10})
            return out
        }
        if (status === "error") {
            if (prefixed)
                out.push({id: "retry", title: "Повторить загрузку каталога", subtitle: error, icon: "refresh", score: 10})
            return out
        }
        const generic = ["плагины", "плагин", "plugins", "plugin"].includes(q)
        for (const entry of entries) {
            const hay = [entry.id, entry.name, entry.description, entry.author, entry.category, ...(entry.tags || [])].join(" ").toLowerCase()
            if (q && !generic && !hay.includes(q))
                continue
            const local = Plugins.byId(entry.id)
            out.push({id: "plugin:" + entry.id, title: entry.name,
                      subtitle: (local ? "Установлен v" + local.version : "Доступен v" + entry.version) + " · " + (entry.author || "Community") + " · Enter — карточка в Market",
                      icon: entry.icon || "package", score: q && String(entry.name).toLowerCase().startsWith(q) ? 160 : 110})
        }
        return out.slice(0, 30)
    }
    function activate(id) {
        if (id === "retry") { fetch(); return true }
        if (id === "loading") return true
        if (id === "publish") {
            Shell.openSettings("plugin:community-store", "publish")
        } else if (String(id).startsWith("plugin:")) {
            Shell.openSettings("plugin:community-store", String(id).slice(7))
        }
        return false
    }
    Process {
        id: reader
        stdout: StdioCollector { id: output }
        stderr: StdioCollector { id: errors }
        onExited: code => {
            try {
                if (code !== 0) throw new Error(errors.text.trim() || "Не удалось загрузить каталог")
                const payload = JSON.parse(output.text)
                root.entries = payload.plugins.filter(entry => entry && entry.status === "approved")
                root.status = "ready"
            } catch (e) {
                root.error = String(e)
                root.status = "error"
            }
            root.changed()
        }
    }
}
