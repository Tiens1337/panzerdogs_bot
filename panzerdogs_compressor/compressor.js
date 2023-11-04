var e = String.fromCharCode,
  t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
  n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$",
  a = {};
function i(e, t) {
  if (!a[e]) {
    a[e] = {};
    for (var n = 0, i = e.length; n < i; n++) a[e][e.charAt(n)] = n;
  }
  return a[e][t];
}
var o = {
  compressToBase64: function (e) {
    if (null == e) return "";
    var n = o._compress(e, 6, function (e) {
      return t.charAt(e);
    });
    switch (n.length % 4) {
      default:
      case 0:
        return n;
      case 1:
        return n + "===";
      case 2:
        return n + "==";
      case 3:
        return n + "=";
    }
  },
  decompressFromBase64: function (e) {
    return null == e
      ? ""
      : "" == e
      ? null
      : o._decompress(e.length, 32, function (n) {
          return i(t, e.charAt(n));
        });
  },
  compressToUTF16: function (t) {
    return null == t
      ? ""
      : o._compress(t, 15, function (t) {
          return e(t + 32);
        }) + " ";
  },
  decompressFromUTF16: function (e) {
    return null == e
      ? ""
      : "" == e
      ? null
      : o._decompress(e.length, 16384, function (t) {
          return e.charCodeAt(t) - 32;
        });
  },
  compressToUint8Array: function (e) {
    for (
      var t = o.compress(e),
        n = new Uint8Array(2 * t.length),
        a = 0,
        i = t.length;
      a < i;
      a++
    ) {
      var r = t.charCodeAt(a);
      (n[2 * a] = r >>> 8), (n[2 * a + 1] = r % 256);
    }
    return n;
  },
  decompressFromUint8Array: function (t) {
    if (null == t) return o.decompress(t);
    for (var n = new Array(t.length / 2), a = 0, i = n.length; a < i; a++)
      n[a] = 256 * t[2 * a] + t[2 * a + 1];
    var r = [];
    return (
      n.forEach(function (t) {
        r.push(e(t));
      }),
      o.decompress(r.join(""))
    );
  },
  compressToEncodedURIComponent: function (e) {
    return null == e
      ? ""
      : o._compress(e, 6, function (e) {
          return n.charAt(e);
        });
  },
  decompressFromEncodedURIComponent: function (e) {
    return null == e
      ? ""
      : "" == e
      ? null
      : ((e = e.replace(/ /g, "+")),
        o._decompress(e.length, 32, function (t) {
          return i(n, e.charAt(t));
        }));
  },
  compress: function (t) {
    return o._compress(t, 16, function (t) {
      return e(t);
    });
  },
  _compress: function (e, t, n) {
    if (null == e) return "";
    var a,
      i,
      o,
      r,
      c = {},
      s = {},
      d = "",
      l = "",
      f = "",
      u = 2,
      p = 3,
      b = 2,
      m = [],
      g = 0,
      h = 0;
    for (o = 0, r = e.length; o < r; o += 1)
      if (
        ((d = e.charAt(o)),
        Object.prototype.hasOwnProperty.call(c, d) ||
          ((c[d] = p++), (s[d] = !0)),
        (l = f + d),
        Object.prototype.hasOwnProperty.call(c, l))
      )
        f = l;
      else {
        if (Object.prototype.hasOwnProperty.call(s, f)) {
          if (f.charCodeAt(0) < 256) {
            for (a = 0; a < b; a++)
              (g <<= 1), h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++;
            for (i = f.charCodeAt(0), a = 0; a < 8; a++)
              (g = (g << 1) | (1 & i)),
                h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
                (i >>= 1);
          } else {
            for (i = 1, a = 0; a < b; a++)
              (g = (g << 1) | i),
                h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
                (i = 0);
            for (i = f.charCodeAt(0), a = 0; a < 16; a++)
              (g = (g << 1) | (1 & i)),
                h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
                (i >>= 1);
          }
          0 == --u && ((u = Math.pow(2, b)), b++), delete s[f];
        } else
          for (i = c[f], a = 0; a < b; a++)
            (g = (g << 1) | (1 & i)),
              h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
              (i >>= 1);
        0 == --u && ((u = Math.pow(2, b)), b++), (c[l] = p++), (f = String(d));
      }
    if ("" !== f) {
      if (Object.prototype.hasOwnProperty.call(s, f)) {
        if (f.charCodeAt(0) < 256) {
          for (a = 0; a < b; a++)
            (g <<= 1), h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++;
          for (i = f.charCodeAt(0), a = 0; a < 8; a++)
            (g = (g << 1) | (1 & i)),
              h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
              (i >>= 1);
        } else {
          for (i = 1, a = 0; a < b; a++)
            (g = (g << 1) | i),
              h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
              (i = 0);
          for (i = f.charCodeAt(0), a = 0; a < 16; a++)
            (g = (g << 1) | (1 & i)),
              h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
              (i >>= 1);
        }
        0 == --u && ((u = Math.pow(2, b)), b++), delete s[f];
      } else
        for (i = c[f], a = 0; a < b; a++)
          (g = (g << 1) | (1 & i)),
            h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
            (i >>= 1);
      0 == --u && ((u = Math.pow(2, b)), b++);
    }
    for (i = 2, a = 0; a < b; a++)
      (g = (g << 1) | (1 & i)),
        h == t - 1 ? ((h = 0), m.push(n(g)), (g = 0)) : h++,
        (i >>= 1);
    for (;;) {
      if (((g <<= 1), h == t - 1)) {
        m.push(n(g));
        break;
      }
      h++;
    }
    return m.join("");
  },
  decompress: function (e) {
    return null == e
      ? ""
      : "" == e
      ? null
      : o._decompress(e.length, 32768, function (t) {
          return e.charCodeAt(t);
        });
  },
  _decompress: function (t, n, a) {
    var i,
      o,
      r,
      c,
      s,
      d,
      l,
      f = [],
      u = 4,
      p = 4,
      b = 3,
      m = "",
      g = [],
      h = { val: a(0), position: n, index: 1 };
    for (i = 0; i < 3; i += 1) f[i] = i;
    for (r = 0, s = Math.pow(2, 2), d = 1; d != s; )
      (c = h.val & h.position),
        (h.position >>= 1),
        0 == h.position && ((h.position = n), (h.val = a(h.index++))),
        (r |= (c > 0 ? 1 : 0) * d),
        (d <<= 1);
    switch (r) {
      case 0:
        for (r = 0, s = Math.pow(2, 8), d = 1; d != s; )
          (c = h.val & h.position),
            (h.position >>= 1),
            0 == h.position && ((h.position = n), (h.val = a(h.index++))),
            (r |= (c > 0 ? 1 : 0) * d),
            (d <<= 1);
        l = e(r);
        break;
      case 1:
        for (r = 0, s = Math.pow(2, 16), d = 1; d != s; )
          (c = h.val & h.position),
            (h.position >>= 1),
            0 == h.position && ((h.position = n), (h.val = a(h.index++))),
            (r |= (c > 0 ? 1 : 0) * d),
            (d <<= 1);
        l = e(r);
        break;
      case 2:
        return "";
    }
    for (f[3] = l, o = l, g.push(l); ; ) {
      if (h.index > t) return "";
      for (r = 0, s = Math.pow(2, b), d = 1; d != s; )
        (c = h.val & h.position),
          (h.position >>= 1),
          0 == h.position && ((h.position = n), (h.val = a(h.index++))),
          (r |= (c > 0 ? 1 : 0) * d),
          (d <<= 1);
      switch ((l = r)) {
        case 0:
          for (r = 0, s = Math.pow(2, 8), d = 1; d != s; )
            (c = h.val & h.position),
              (h.position >>= 1),
              0 == h.position && ((h.position = n), (h.val = a(h.index++))),
              (r |= (c > 0 ? 1 : 0) * d),
              (d <<= 1);
          (f[p++] = e(r)), (l = p - 1), u--;
          break;
        case 1:
          for (r = 0, s = Math.pow(2, 16), d = 1; d != s; )
            (c = h.val & h.position),
              (h.position >>= 1),
              0 == h.position && ((h.position = n), (h.val = a(h.index++))),
              (r |= (c > 0 ? 1 : 0) * d),
              (d <<= 1);
          (f[p++] = e(r)), (l = p - 1), u--;
          break;
        case 2:
          return g.join("");
      }
      if ((0 == u && ((u = Math.pow(2, b)), b++), f[l])) m = f[l];
      else {
        if (l !== p) return null;
        m = o + o.charAt(0);
      }
      g.push(m),
        (f[p++] = o + m.charAt(0)),
        (o = m),
        0 == --u && ((u = Math.pow(2, b)), b++);
    }
  },
}

module.exports = { o };
