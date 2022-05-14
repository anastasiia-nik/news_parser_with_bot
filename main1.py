from dataclasses import dataclass


@dataclass
class Email:
    subject: str
    sender: str
    receiver: str
    text: str
    attach: list[str] = lambda: []

class BaseObject:
    def __init__(self, email):
        self.email = email
        self.weight=0

class BaseWeight:
    def __init__(self, obj, weight=0):
        self._obj = obj
        self.rule_weight = weight

    @property
    def obj(self):
        return self._obj

    @property
    def email(self):
        return self.obj.email

    def set_property(self, **kwars):
        self.myproperty = kwars
        return self

class CheckSenders(BaseWeight):

    @property
    def weight(self):
        email = self.email
        if len(self.email.sender.split(',')) > self.myproperty['kvo']:
            return self.obj.weight + self.rule_weight
        return self.obj.weight

class CheckReceiver(BaseWeight):
    @property
    def weight(self):
        if len(self.email.receiver.split(',')) > self.myproperty['rcvrcount']:
            return self.obj.weight + self.rule_weight
        return self.obj.weight

email = Email(
    "qwe", "qwe", "qwe", "qwe",
)


start = BaseObject(email)

b2 = CheckSenders(start, 20)
b2.set_property(**{'kvo': 5})
b3 = CheckReceiver(b2, 30)
b3.set_property(**{'rcvrcount': 3})

print(b3.weight)



email2 = Email('qwe', "qwe,1,1,1,1,1,1,1,1,1,1", "3,3,3,3,3q,w,e,", "qwe", "fsdf")
start.email = email2
print(b3.weight)
exit(0)


class Product:
    price = 10


class Cream:
    def __init__(self, obj: Product):
        self.obj = obj

    @property
    def price(self):
        return self.obj.price + 10


class Cinnamon:
    def __init__(self, obj: Product):
        self.obj = obj

    @property
    def price(self):
        return self.obj.price + 5


class Milk:
    def __init__(self, obj: Product):
        self.obj = obj

    @property
    def price(self):
        return self.obj.price + 14


product = Product()
c1 = Cream(product)
c2 = Cinnamon(c1)
print(c2.price)

product.price = 100
print(c2.price)

exit(0)


def decor(func):
    details = 0

    def wrapper(*args, **kwargs):
        nonlocal details
        details += 1
        print(f"Function {func.__name__} {details}")
        return func(*args, **kwargs)

    return wrapper


exit(0)


class Exchanger:
    course = 30

    def __init__(self):
        self.subscribers = {}

    def set_course(self, val):
        self.course = val
        for author in self.subscribers:
            # print(f"Notify {author}")
            func = self.subscribers[author]
            func(val)

    def get_course(self):
        return self.course

    def subscribe(self, author: str, func: callable):
        self.subscribers[author] = func

    def unsubscribe(self, author: str):
        if author in self.subscribers:
            self.subscribers.pop(author)


class Listener:
    def subscribe_to_cours(self, exch: Exchanger):
        exch.subscribe(str(id(self)), self.new_course_set)
        return self

    def unsubscribe_from_cours(self, exch: Exchanger):
        exch.unsubscribe(str(id(self)))
        return self


class MobileCllient(Listener):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def new_course_set(self, val):
        print(f"{self.name} call to {self.phone} new course is {val}")


class TGCllient(Listener):
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def new_course_set(self, val):
        print(f"send msg to {self.chat_id} new course is {val}")


exch = Exchanger()
MobileCllient('aaa', '123456').subscribe_to_cours(exch)
MobileCllient('bbbb', '2342346').subscribe_to_cours(exch)
TGCllient('bbbb', ).subscribe_to_cours(exch)

exch.set_course(28)

exit(0)


class Action:
    radius = 0
    strength = 0


class Novice(Action):
    radius = 1
    strength = 2


class MidlePla(Action):
    radius = 2
    strength = 5


class Trauma(Action):
    radius = 1
    strength = 1


class Player:
    name: str
    x, y = 0, 0
    steps_count = 0

    def __init__(self, name, action: Action):
        self.name = name
        self.lvl = action

    def set_new_action(self, action: Action):
        self.lvl = action

    def kick(self, obj: 'Player'):
        self.lvl.radius
        if False:
            self.set_state_after(5, elf.lvl)
            self.lvl = Trauma()

    def set_state_after(self, step, state):
        self.__step_to_new_state = step
        self.__new_state = state

    def apply_new_state(self):
        if self.__step_to_new_state > 0:
            self.__step_to_new_state -= 1
            return
        if self.__new_state is not None:
            self.lvl = self.__new_state
            self.__new_state = None

    def step(self):
        self.steps_count += 1
        self.apply_new_state()


p1 = Player("User 1", Novice())
