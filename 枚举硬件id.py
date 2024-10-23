def get_devices(self):
    return self.system_device_enum.get_available_filters2(DeviceCategories.VideoInputDevice)

def get_available_filters2(self, category_clsid: str):
    filter_enumerator = self.system_device_enum.CreateClassEnumerator(GUID(category_clsid), dwFlags=0)
    result: list[str] = []
    try:
        moniker, count = filter_enumerator.Next(1)
    except ValueError:
        return result
    while count > 0:
        result.append(get_moniker_hardware_id(moniker))
        moniker, count = filter_enumerator.Next(1)
    return result

def get_moniker_hardware_id(moniker: IMONIKER) -> str:
    try:
        property_bag = moniker.BindToStorage(0, 0, IPropertyBag._iid_).QueryInterface(IPropertyBag)
        DevicePath = property_bag.Read("DevicePath", pErrorLog=None)
        DevicePath = DevicePath.split("#")
        if len(DevicePath) < 2:
            return ""
        vid_pid = DevicePath[1].split("&")
        if len(vid_pid) < 2:
            return ""
        vid = vid_pid[0]
        pid = vid_pid[1]
        pid = pid.replace("pid_", "")
        return pid
    except COMError as e:
        print(f"An error occurred: {e}")
        return ""




from pygrabber.dshow_graph import FilterGraph


def  getCamerIndex(pid)->int:
    graph = FilterGraph()
    evices =graph.get_devices()
    print(evices)
    #返回pid在tuplesss的序号
    for index in range(len(evices)):
        if pid in evices[index]:
            return index



if __name__ == '__main__':
    print(getCamerIndex("2130"))
