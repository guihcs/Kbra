
draw_river = """
reset()
#cc 164, 255, 68


learn drawFlower $x, $y{
  $posx = getx()
  $posy = gety()
  $dir = getdir()
  go($x, $y)
  pc(0, 220, 0)
  pw(5)
  fw(16)
  tr(90)
  fw(3)
  bw(3)
  tl(90)
  fw(4)
  pc(200,0,0)
  pu()
  fw(8)
  tl(90)
  pw(10)
  fw(2)
  pd()
  fw(2)
  dir(0)
  go($posx, $posy)
  dir($dir)
}

learn drawTree $x, $y{
  $posx = getx()
  $posy = gety()
  $dir = getdir()
  go($x, $y)
  pc(90, 60, 40)
  pw(15)
  fw(20)
  pc(0,200,0)
  pu()
  fw(20)
  tl(90)
  pw(25)
  bw(5)
  pd()
  fw(12)
  dir(0)
  go($posx, $posy)
  dir($dir)
}

learn drawRiver $y{
  $posx = getx()
  $posy = gety
  $dir = getdir()
  pc(60, 200, 240)
  go(30, $y)
  tr(90)
  pw(60)
  fw(340)  
  dir(0)
  go($posx, $posy)
  dir($dir)
}
learn drawFish $x, $y, $r,$g,$b{
  $posx = getx()
  $posy = gety()
  $dir = getdirection()
  go($x, $y)
  dir(0)
  pw(2)
  pc($r,$g,$b)
  tr(60)
  fw(20)
  tr(60)
  fw(10)
  tr(120)
  fw(10)
  tr(60)
  fw(20)
  dir(180)
  fw(10)
  go($posx, $posy)
  dir($dir)
}
#setup
$x = 0
$y = random(200, 250)
$r = random(0, 255)
$g = random(0, 255)
$b = random(0, 255)
$var = random(0, 20)
$havFish = false
$x2 = 0
$y2 = random(200, 250)
$r2 = random(0, 255)
$g2 = random(0, 255)
$b2 = random(0, 255)
$var2 = random(0, 20)

while true {
  $x = $x + 5
  $x2 = $x2 + 5
  if $x2 >= 390{
    $havFish = false
    $y2 = random(200, 250)
    $x2 = 0
    $r2 = random(0, 255)
    $g2 = random(0, 255)
    $b2 = random(0, 255)
    $var2 = random(0, 10)
  }
  if $x >= 390 {
    $x = 0
    $r = random(0, 255)
    $g = random(0, 255)
    $b = random(0, 255)

    $y = random(200, 250)
    $var = random(0, 10)
  }

  sh()
  drawTree(80, 150)
  drawTree(250, 100)
  drawTree(320, 360)
  drawFlower(80, 350)
  drawFlower(280, 170)
  drawRiver(220)
  drawFish($x, $y, $r,$g,$b)
  if $x > 30 {drawFish($x - 65, $y + $var,   $g,$r,$b)  }
  if $x2 > 30 {drawFish( $x2 - 45, $y2 + $var2, $g2,$b2,$r2)  }
  if $x > 160 and not $havFish{
    $havFish = true
    $x2 = 0
  }
  if $havFish {
    drawFish($x2, $y2, $r2,$g2,$b2)
  }
  print("Happy day...")
  ss()
  go(200, 270)
  wait(0.1)
  clear()
  
  dir(0)
}
"""