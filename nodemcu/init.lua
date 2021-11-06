id  = i2c.SW
sda = 21
scl = 22

i2c.setup(id, sda, scl, i2c.SLOW)

--[[
for i=0,127 do
  i2c.start(id)
  resCode = i2c.address(id, i, i2c.TRANSMITTER)
  i2c.stop(id)
  if resCode == true then
	print("We have a device on address 0x" .. string.format("%02x", i) .. " (" .. i ..")")
  end
end
]]--

-- https://github.com/yakumo-saki/nodemcu-lua-sh1106-example/blob/master/dumpdisplay.lua
sla1 = 0x3c
dis1 = u8g2.ssd1306_i2c_128x64_noname(id, sla1)

-- dis1:setFlipMode(1) -- turn image upside down
dis1:clearBuffer()
dis1:setContrast(255)
dis1:setFontMode(0)
dis1:setDrawColor(1)
dis1:setBitmapMode(0)
dis1:setFont(u8g2.font_6x10_tf)

-- draw some frames and boxes
dis1:drawFrame(0, 0, 128, 64)
dis1:drawBox(20, 20, 30, 40)
dis1:drawStr(2, 12, "NodeMCU ftw")
dis1:sendBuffer()

sla2 = 0x3d
dis2 = u8g2.ssd1306_i2c_128x64_noname(id, sla2)
-- dis2:setFlipMode(1) -- turn image upside down
dis2:clearBuffer()
dis2:setContrast(255)
dis2:setFontMode(0)
dis2:setDrawColor(1)
dis2:setBitmapMode(0)
dis2:setFont(u8g2.font_6x10_tf)

dis2:drawFrame(0, 0, 128, 64)
dis2:drawBox(70, 20, 40, 30)
dis2:drawStr(2, 32, "das Labor")
dis2:sendBuffer()

-- turn the LED on
gpio.config({ gpio=4, dir=gpio.OUT }, { gpio={0,2}, dir=gpio.IN, pull=gpio.PULL_UP })
x = 1
gpio.write(4, x)

-- https://nodemcu.readthedocs.io/en/dev-esp32/modules/mqtt/#mqttclientpublish
server = "mqtt.das-labor.org"
user = "USER"
pass = "PASS"
topic = "/labortagetest"

m = mqtt.Client("clientid", 120, user, pass)

-- on publish message receive event
m:on("message", function(client, topic, data)
  print(topic .. ":")
  if data ~= nil then
    print(data)
    if data == "trig" then
      if x == 0 then
        x = 1
      else
        x = 0
      end
      gpio.write(4, x)
    end
    if data == "pew" then
      dis1:drawStr(2, 12, "pew")
      dis1:sendBuffer()
    end
    if data == "zap" then
      dis1:drawStr(2, 12, "zap")
      dis1:sendBuffer()
    end
  end
end)

function handle_mqtt_connect(client)
  print ("connected")
  client:subscribe(topic, 0, function(client) print("subscribe success") end)
	function send_msg()
		client:publish(topic, "hello", 0, 0, function(client) print("sent") end)
	end
	function send_trig()
		client:publish(topic, "trig", 0, 0, function(client) print("sent") end)
	end
	function send_zap()
		client:publish(topic, "zap", 0, 0, function(client) print("sent") end)
	end
	function send_pew()
		client:publish(topic, "pew", 0, 0, function(client) print("sent") end)
	end
  gpio.trig(0, gpio.INTR_LOW, send_pew)
  gpio.trig(2, gpio.INTR_LOW, send_zap)
  tmr.create():alarm(10 * 1000, tmr.ALARM_SINGLE, send_msg)
end

function handle_mqtt_error(client, reason)
  tmr.create():alarm(10 * 1000, tmr.ALARM_SINGLE, do_mqtt_connect)
end

function do_mqtt_connect()
  m:connect(server, handle_mqtt_connect, handle_mqtt_error)
end

-- https://nodemcu.readthedocs.io/en/dev-esp32/modules/wifi/#wifistaconfig
--connect to Access Point (DO save config to flash)
wifi.start()
wifi.mode(wifi.STATION, true)

station_cfg={}
station_cfg.ssid="l1"
station_cfg.pwd="blafoo234211sicher"
wifi.sta.config(station_cfg, true)

--register callback
wifi.sta.on("got_ip", function(ev, info)
  print("NodeMCU IP config:", info.ip, "netmask", info.netmask, "gw", info.gw)
  do_mqtt_connect()
end)

wifi.sta.connect()
