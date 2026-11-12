local M = {count = 0}
local function glyphs(head, out)
  out = out or {}
  for n in node.traverse(head) do
    if n.id == node.id('glyph') then
      out[#out + 1] = {font = n.font, char = n.char}
    elseif n.id == node.id('hlist') or n.id == node.id('vlist') then
      glyphs(n.head, out)
    end
  end
  return out
end
-- a, A, alpha, Gamma, partial, nabla, 1: independent expected Unicode slots.
local slots = {
  [0] = {0x1D44E,0x1D434,0x1D6FC,0x1D6E4,0x1D715,0x1D6FB,0x31},
  [1] = {0x1D482,0x1D468,0x1D736,0x1D71E,0x1D74F,0x1D735,0x1D7CF},
  [4] = {0x61,0x41,0x3B1,0x393,0x2202,0x2207,0x31},
  [5] = {0x1D41A,0x1D400,0x1D6C2,0x1D6AA,0x1D6DB,0x1D6C1,0x1D7CF},
}
function M.check(state)
  local gs = glyphs(tex.box[0].head)
  local expected = slots[state & 5]
  assert(#gs == #expected, 'Unexpected glyph count')
  local family = (state & 2) == 0 and 'NewCMMath-Regular' or 'NewCMSansMath-Regular'
  for i, g in ipairs(gs) do
    local f = font.getfont(g.font)
    local cp, filename = expected[i], family
    if (state & 8) ~= 0 then
      filename = 'NewCMMath-Regular'
      if i <= 4 or i == 7 then
        cp = ({0x61,0x41,0x3B1,0x393,0,0,0x31})[i]
        local face = (state & 1) ~= 0
          and (((state & 4) ~= 0 or i == 7) and 'Bold' or 'BoldOblique')
          or (((state & 4) ~= 0 or i == 7) and 'Regular' or 'Italic')
        filename = 'NewCMMono10-'..face
        if i ~= 3 and i ~= 4 then
          -- Latin letters and digits use the proportional typewriter.
          filename = ({Regular = 'lmmonoprop10-regular',
            Italic = 'lmmonoprop10-oblique',
            Bold = 'lmmonoproplt10-bold',
            BoldOblique = 'lmmonoproplt10-boldoblique'})[face]
        end
      end
    end
    assert(g.char == cp, string.format(
      'State %d glyph %d: U+%X, expected U+%X', state, i, g.char, cp))
    assert(f.filename:find(filename..'.otf', 1, true), 'Wrong font: '..f.filename)
    assert(f.characters[g.char], 'Missing glyph')
  end
  M.count = M.count + 1
end
function M.oldstyle()
  local a, b = glyphs(tex.box[0].head), glyphs(tex.box[1].head)
  assert(#a == 10 and #b == 10, 'Expected ten text digits')
  for i, g in ipairs(a) do
    local fa, fb = font.getfont(g.font), font.getfont(b[i].font)
    assert(fa.characters[g.char].index ~= fb.characters[b[i].char].index,
      'Oldstyle feature did not change digit '..(i-1)..' in '..fa.filename)
  end
  M.count = M.count + 1
end
function M.textgreek()
  local a, b = glyphs(tex.box[0].head), glyphs(tex.box[1].head)
  assert(#a == #b and #a == 49, 'Expected complete text Greek alphabet')
  for i, g in ipairs(a) do
    local f = font.getfont(g.font)
    assert(g.char == b[i].char and g.font == b[i].font,
      'Greek text command differs from literal at '..i)
    assert(f.characters[g.char], 'Missing text Greek glyph')
  end
  M.count = M.count + 1
end
function M.monogreek(expected, face)
  local gs = glyphs(tex.box[0].head)
  local i = 0
  for _, cp in utf8.codes(expected) do
    i = i + 1
    local g = assert(gs[i], 'Missing mono Greek character')
    local f = font.getfont(g.font)
    assert(g.char == cp, 'Wrong mono Greek mapping at '..i)
    assert(f.filename:find('NewCMMono10-'..face..'.otf', 1, true), 'Wrong mono Greek face')
    assert(f.characters[g.char], 'Missing mono Greek glyph')
  end
  assert(#gs == i, 'Unexpected mono Greek glyph count')
  M.count = M.count + 1
end
function M.equal()
  local a, b = glyphs(tex.box[0].head), glyphs(tex.box[1].head)
  assert(#a == #b, 'Scope/structure: different glyph counts')
  for i, g in ipairs(a) do
    assert(g.font == b[i].font and g.char == b[i].char,
      'Scope/structure: different glyph at '..i)
  end
  assert(tex.box[0].width == tex.box[1].width, 'Different math spacing')
  assert(tex.box[0].height == tex.box[1].height, 'Different height')
  assert(tex.box[0].depth == tex.box[1].depth, 'Different depth')
  M.count = M.count + 1
end
function M.differ()
  local a, b = glyphs(tex.box[0].head), glyphs(tex.box[1].head)
  local same = #a == #b
  for i, g in ipairs(a) do
    same = same and g.font == b[i].font and g.char == b[i].char
  end
  assert(not same, 'Expected different glyphs')
  M.count = M.count + 1
end
-- Different glyphs of the font files, so that a stylistic set took effect.
function M.glyphdiffer()
  local a, b = glyphs(tex.box[0].head), glyphs(tex.box[1].head)
  assert(#a == #b, 'Expected the same number of glyphs')
  for i, g in ipairs(a) do
    local fa, fb = font.getfont(g.font), font.getfont(b[i].font)
    assert(fa.characters[g.char].index ~= fb.characters[b[i].char].index,
      'Expected different glyph indices at '..i)
  end
  M.count = M.count + 1
end
return M
