from utils.Parser import Term


def is_var(term: Term):
    return term.type == 'var'


def is_str(term: Term):
    return term.type =='constr' or term.type == 'const'

class Entry:
    def __init__(self, term: str, functor: str, type: str):
        self.term = term
        self.functor = functor
        self.components = []
        self.type = type

    def get_arity(self):
        return len(self.components)


def is_constr(entry: Entry):
    return entry.type == 'constr'


class UnifTable:
    def __init__(self, terms):
        self.terms = terms
        self.look_up = dict()  # [str]int
        self.bindings = dict()  # [int]int
        self.entries = []
        i = 0
        for n in range(len(terms)-1, -1, -1):
            t = self.terms[n]
            if t.s in self.look_up:
                continue

            e = Entry(
                t.s,
                t.name,
                t.type
            )
            for c in t.args:
                assert c.s in self.look_up
                idx = self.look_up[c.s]
                e.components.append(idx)

            self.look_up[t.s] = i
            self.entries.append(e)
            i += 1

    def unify(self, ix, iy) -> bool:
        sx, sy = [ix], [iy]

        while len(sx) and len(sy):
            ix = sx.pop()
            iy = sy.pop()
            ex = self.entries[ix]
            ey = self.entries[iy]


            # case 1
            if is_str(ex) and is_str(ey):
                ax = ex.get_arity()
                ay = ey.get_arity()
                if ex.functor != ey.functor or ax != ay:
                    return False
                if ax > 0:
                    sx.extend(ex.components)
                    sy.extend(ey.components)

            # case 2
            elif is_str(ex) and is_var(ey):
                idx, _, b = self.bind_str(ix, iy)
                if not b:
                    sx.append(ix)
                    sy.append(idx)


            # case 3
            elif is_var(ex) and is_str(ey):
                idx, _, b = self.bind_str(iy, ix)
                if not b:
                    sx.append(idx)
                    sy.append(iy)


            # case 4
            elif is_var(ex) and is_var(ey):
                idx1, idx2, b = self.bind_var(ix, iy)
                if not b:
                    sx.append(idx1)
                    sx.append(idx2)


        return True

    def dereference(self, idx) -> int:
        i = idx
        ok = True
        while ok:
            if i in self.bindings:
                i = self.bindings[i]
                idx = i
            else:
                ok = False
        return idx


    def bind_var(self, var_idx1, var_idx2) -> (int, int, bool):
        i1 = 0
        i2 = 0
        f1 = False
        f2 = False
        if var_idx1 in self.bindings:
            i1 = self.bindings[var_idx1]
            f1 = 1
        if var_idx2 in self.bindings:
            i2 = self.bindings[var_idx2]
            f2 = 1

        if not f1 and not f2:
            self.bindings[var_idx1] = var_idx2
            return var_idx1, var_idx2, True

        if f1 and not f2:
            self.bindings[var_idx2] = var_idx1
            return var_idx1, var_idx2, True

        return i1, i2, False

    def term_string(self, idx) -> str:
        if idx >= len(self.entries):
            return ''

        e = self.entries[idx]
        if is_constr(e):
            return e.functor

        components = []
        for c in e.components:
            i = self.dereference(c)
            if i != idx and is_constr(self.entries[i]):
                components.append(self.term_string(i))
            else:
                components.append(self.entries[i].functor)

        return self.entries[idx].functor + '(' + ','.join(components) + ')'

    def bind_str(self, str_idx, var_idx) -> (int, int, bool):
        if not var_idx in self.bindings:
            self.bindings[var_idx] = str_idx
            return str_idx, var_idx, True

        idx = self.bindings[var_idx]
        idx = self.dereference(idx)

        e = self.entries[idx]
        if is_str(e):
            return idx, var_idx, False

        self.bindings[var_idx] = idx
        return idx, var_idx, True


def unify(x: Term, y: Term) -> dict:
    terms = x.unfold() + y.unfold()
    ut = UnifTable(terms)

    ix, iy = ut.look_up[x.s], ut.look_up[y.s]
    if not ut.unify(ix, iy):
        return None

    mgu = dict()
    for i, j in ut.bindings.items():
        j = ut.dereference(j)
        mgu[ut.entries[i].functor] = ut.term_string(j)
    return mgu
