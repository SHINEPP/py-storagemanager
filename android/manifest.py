import os
import re
import xml.etree.ElementTree as ET

NS_ANDROID = 'http://schemas.android.com/apk/res/android'
NS_APP = 'http://schemas.android.com/apk/res-auto'
NS_TOOLS = 'http://schemas.android.com/tools'

NS_DICT = {NS_ANDROID: 'android', NS_APP: 'app', NS_TOOLS: 'tools'}


class XmlFormatter:

    def __init__(self, sources):
        self.sources = sources
        self.namespace = {}
        self.elements = []
        self.last_element = None
        self.pattern = re.compile(r'\{(.+)}(.+)')

    def format(self, text):
        self.namespace.clear()
        self.elements.clear()
        self.last_element = None

        root = ET.fromstring(text)
        self._handle_namespace(root)

        self._handle_element(root, 0, 0)

    def _handle_namespace(self, root):
        attrib = root.attrib
        for attr_key in attrib:
            match = self.pattern.match(attr_key)
            if match:
                name = match[1]
                if name in NS_DICT and name not in self.namespace:
                    self.namespace[name] = NS_DICT[name]
        for element in root:
            self._handle_namespace(element)

    def _handle_element(self, root, level, index):
        # tag start
        tag = root.tag
        parent = None
        if len(self.elements) > 0:
            parent = self.elements[-1]

        self.elements.append(root)
        self.last_element = root

        component = ''
        # 属性
        attrib = root.attrib
        for key in attrib:
            name = self._get_attr_name_alize(key)
            if tag in ('instrumentation', 'application', 'provider', 'service', 'receiver', 'activity'):
                if name == 'android:name':
                    component = attrib[key]
            elif tag == 'activity-alias':
                if name == 'android:targetActivity':
                    component = attrib[key]
        if component:
            class_path = component.replace('.', os.path.sep) + '.java'
            path = os.path.join(self.sources, class_path)
            exists = os.path.exists(path)
            print(f'{component} -> {exists}')

        # 处理子元素
        i = -1
        for element in root:
            i += 1
            self._handle_element(element, level + 1, i)

        # tag end
        self.last_element = root
        self.elements.pop()

    def _get_attr_name_alize(self, key):
        """
        判读是否使用namespace, 如何存在则返回别名, 其他则key
        :param key:
        :return:
        """
        match = self.pattern.match(key)
        if match:
            name1, name2 = match[1], match[2]
            if name1 in self.namespace:
                alize = self.namespace[name1]
                return f'{alize}:{name2}'
        return key


if __name__ == '__main__':
    r_path = '/Users/zhouzhenliang/Desktop/apk/deepsafebrowser/deepsafebrowser-vc4-v1.2.0-release'
    mf_path = os.path.join(r_path, 'resources/base/manifest/AndroidManifest.xml')
    s_path = os.path.join(r_path, 'sources')
    with open(mf_path, 'r') as file:
        XmlFormatter(s_path).format(file.read())
