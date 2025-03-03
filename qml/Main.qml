import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 300
    height: 200
    visible: true
    title: "Hello World"

    readonly property list<string> texts: ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
    property int ind: 0


    function setText() {
        text.text = texts[ind] + " ind: " + ind++
        if(ind >= 4){
            ind = 0
        }
    }

    ColumnLayout {
        anchors.fill:  parent

        Text {
            id: text
            text: "Hello World"
            Layout.alignment: Qt.AlignHCenter
        }
        Button {
            text: "Click me"
            Layout.alignment: Qt.AlignHCenter
            onClicked: setText()
        }
    }
}