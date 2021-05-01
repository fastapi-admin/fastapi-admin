class ClassProperty(property):
    def __get__(self, obj, obj_type=None):
        return super(ClassProperty, self).__get__(obj_type)

    def __set__(self, obj, value):
        super(ClassProperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(ClassProperty, self).__delete__(type(obj))
