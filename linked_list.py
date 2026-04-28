class DoAn:
    def __init__(self, ma: str, ten: str, mssv: str, hoten: str,
                 gvhd: str, lop: str, namhoc: str, trangthai: str, diem: float):
        self.ma = ma.strip()
        self.ten = ten.strip()
        self.mssv = mssv.strip()
        self.hoten = hoten.strip()
        self.gvhd = gvhd.strip()
        self.lop = lop.strip()
        self.namhoc = namhoc.strip()
        self.trangthai = trangthai.strip()
        self.diem = float(diem)
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None

    def them(self, doan):
        if self.tim_theo_ma(doan.ma) or self.tim_theo_mssv(doan.mssv):
            return False
        if not self.head:
            self.head = doan
            return True
        current = self.head
        while current.next:
            current = current.next
        current.next = doan
        return True

    def tim_theo_ma(self, ma):
        current = self.head
        while current:
            if current.ma == ma:
                return current
            current = current.next
        return None

    def tim_theo_mssv(self, mssv):
        current = self.head
        while current:
            if current.mssv == mssv:
                return current
            current = current.next
        return None

    def sua(self, ma, doan_moi):
        current = self.head
        while current:
            if current.ma == ma:
                if current.mssv != doan_moi.mssv and self.tim_theo_mssv(doan_moi.mssv):
                    return False
                current.ten = doan_moi.ten
                current.mssv = doan_moi.mssv
                current.hoten = doan_moi.hoten
                current.gvhd = doan_moi.gvhd
                current.lop = doan_moi.lop
                current.namhoc = doan_moi.namhoc
                current.trangthai = doan_moi.trangthai
                current.diem = doan_moi.diem
                return True
            current = current.next
        return False

    def xoa(self, ma):
        if not self.head:
            return False
        if self.head.ma == ma:
            self.head = self.head.next
            return True
        current = self.head
        while current.next:
            if current.next.ma == ma:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current)
            current = current.next
        return result

    def merge_sort(self, head, key=lambda x: x.ma):
        if not head or not head.next:
            return head

        middle = self.get_middle(head)
        next_to_middle = middle.next
        middle.next = None

        left = self.merge_sort(head, key)
        right = self.merge_sort(next_to_middle, key)

        return self.sorted_merge(left, right, key)

    def get_middle(self, head):
        if not head:
            return head
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def sorted_merge(self, left, right, key):
        if not left:
            return right
        if not right:
            return left

        if key(left) <= key(right):
            result = left
            result.next = self.sorted_merge(left.next, right, key)
        else:
            result = right
            result.next = self.sorted_merge(left, right.next, key)
        
        return result

    def sap_xep_merge_theo_ma(self):
        self.head = self.merge_sort(self.head, key=lambda x: x.ma)

    def sap_xep_merge_theo_mssv(self):
        self.head = self.merge_sort(self.head, key=lambda x: x.mssv)

    def sap_xep_merge_theo_ten(self):
        self.head = self.merge_sort(self.head, key=lambda x: x.ten.lower())

    def sap_xep_merge_theo_hoten(self):
        self.head = self.merge_sort(self.head, key=lambda x: x.hoten.lower())

    def sap_xep_merge_theo_lop(self):
        self.head = self.merge_sort(self.head, key=lambda x: x.lop.lower())

    def sap_xep_merge_theo_gvhd(self):
        self.head = self.merge_sort(self.head, key=lambda x: x.gvhd.lower())

    def sap_xep_merge_theo_diem(self, reverse=False):
        self.head = self.merge_sort(self.head, key=lambda x: x.diem)
        if reverse:
            self.dao_nguoc()

    def dao_nguoc(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def sap_xep_theo_trangthai(self):
        lst = self.to_list()
        order = {"Đã báo cáo": 1, "Đã hoàn thành": 2, "Đang thực hiện": 3}
        lst.sort(key=lambda x: order.get(x.trangthai, 99))
        if lst:
            self.head = lst[0]
            current = self.head
            for item in lst[1:]:
                current.next = item
                current = current.next
            current.next = None
