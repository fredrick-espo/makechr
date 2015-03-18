from constants import *


class BinaryOutput(object):
  def __init__(self):
    self._nametable_cache = {}

  def pad(self, fout, num, byte_value=0):
    fout.write(chr(byte_value) * num)

  def save_nametable(self, filename, artifacts):
    fout = open(filename, 'wb')
    for y in xrange(NUM_BLOCKS_Y * 2):
      for x in xrange(NUM_BLOCKS_X * 2):
        nt = artifacts[y][x][ARTIFACT_NT]
        fout.write(chr(nt))
    fout.close()

  def save_chr(self, filename, chr_data):
    fout = open(filename, 'wb')
    for d in chr_data:
      d.write(fout)
    padding = 8192 - (len(chr_data) * 16)
    self.pad(fout, padding)
    fout.close()

  def save_palette(self, filename, palette):
    fout = open(filename, 'wb')
    bg_color = palette.bg_color
    for i in xrange(4):
      palette_option = palette.get(i)
      if palette_option is None:
        palette_option = [bg_color] * 4
      for j in xrange(4):
        if j < len(palette_option):
          fout.write(chr(palette_option[j]))
        else:
          fout.write(chr(bg_color))
    self.pad(fout, 16, bg_color)
    fout.close()

  def save_attribute(self, filename, artifacts):
    fout = open(filename, 'wb')
    for attr_y in xrange(NUM_BLOCKS_Y / 2):
      for attr_x in xrange(NUM_BLOCKS_X / 2):
        y = attr_y * 4
        x = attr_x * 4
        p0 = artifacts[y + 0][x + 0][ARTIFACT_PID]
        p1 = artifacts[y + 0][x + 2][ARTIFACT_PID]
        p2 = artifacts[y + 2][x + 0][ARTIFACT_PID]
        p3 = artifacts[y + 2][x + 2][ARTIFACT_PID]
        attr = p0 + (p1 << 2) + (p2 << 4) + (p3 << 6)
        fout.write(chr(attr))
    self.pad(fout, 8)
    fout.close()
