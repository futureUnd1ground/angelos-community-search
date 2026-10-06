import QtQuick
import qs.config
import qs.services
import qs.widgets

Column {
    property var plugin
    width: parent ? parent.width : Theme.u * 150
    spacing: Theme.u * 4
    PxText {
        width: parent.width
        text: "Ищи название плагина прямо в «Выполнить…». Запрос «market» показывает каталог, «market dog» — результаты по dog. Enter открывает карточку в Community Store."
        wrapMode: Text.Wrap
    }
    Flow {
        width: parent.width
        spacing: Theme.u * 3
        PxButton {
            text: "Открыть Market"
            icon: "package"
            onClicked: Shell.openSettings("plugin:community-store")
        }
        PxButton {
            text: "Опубликовать ZIP"
            icon: "cloud"
            onClicked: Shell.openSettings("plugin:community-store", "publish")
        }
    }
    PxText {
        width: parent.width
        text: "Для публикации: выбери ZIP и нажми «Опубликовать ZIP в Market». Используется вход gh auth login. Исходники и архив становятся публичными на GitHub, а заявка в реестре ждёт одобрения. Повторное нажатие для того же ZIP открывает существующую заявку."
        dim: true
        wrapMode: Text.Wrap
    }
}
