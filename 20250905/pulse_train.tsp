-- 2600BS-901-01F_2600B_Reference_Aug2021.pdf - page 4-21
-- Reset the SourceMeter instrument to default conditions.
reset()
-- configure output offmode 
smua.source.offmode = smua.OUTPUT_ZERO
smub.source.offmode = smub.OUTPUT_ZERO
-- Generate a 10-point pulse train with the following characteristics:
-- * Bias (Idle) Level = 0 V
-- * Pulse Level = 200 mV
-- * Pulse Width = 20 ms
-- * Pulse Period = 100 ms
-- Configure the source function.
smua.source.func = smua.OUTPUT_DCVOLTS
-- Set the voltage source range and the bias source level and limit.
smua.source.rangev = 0.2
smua.source.levelv = 0
smua.source.limiti = 1
-- Use trigger timer 1 to control the period and trigger timer 2 to control the 
-- pulse width. Alias the timers for convenience and clarity.
period_timer = trigger.timer[1]
pulsewidth_timer = trigger.timer[2]
-- Configure the period timer to output 10 total trigger events.
period_timer.delay = 0.1
-- The effective count is 10 because the passthrough setting is true.
period_timer.count = 9
-- Configure the timer to immediately output a trigger event when it is started.
period_timer.passthrough = true
-- Start the timer when the SMU moves from the ARM layer to the TRIGGER layer.
period_timer.stimulus = smua.trigger.ARMED_EVENT_ID
-- Configure the pulse width timer to output one trigger event for each period.
pulsewidth_timer.delay = 0.02
pulsewidth_timer.count = 1
-- Do not immediately output a trigger event when pulse width timer is started.
pulsewidth_timer.passthrough = false
-- Start the pulse width timer with the period timer output trigger event.
pulsewidth_timer.stimulus = period_timer.EVENT_ID
-- Configure the trigger model to execute a 10-point fixed-level voltage pulse 
-- train. No measurements are made.
smua.trigger.source.listv({0.2})
smua.trigger.source.action = smua.ENABLE
smua.trigger.measure.action = smua.DISABLE
-- Set the trigger source limit, which can be different than the bias limit.
-- This is an important setting for pulsing in the extended operating area.
smua.trigger.source.limiti = 1
smua.measure.rangei = 1
-- Trigger SMU source action with the period timer event.
smua.trigger.source.stimulus = period_timer.EVENT_ID
-- Configure the endpulse action to achieve a pulse.
smua.trigger.endpulse.action = smua.SOURCE_IDLE
-- Trigger the SMU end pulse action with a pulse width timer event.
smua.trigger.endpulse.stimulus = pulsewidth_timer.EVENT_ID
-- Set the trigger model count to generate one 10-point pulse train.
smua.trigger.arm.count = 1
smua.trigger.count = 10
-- Turn on the SMU output and initiate the trigger model to output the pulse train.
smua.source.output = smua.OUTPUT_ON
smua.trigger.initiate()
-- Wait for the sweep to complete.
waitcomplete()
-- Turn off SMU output.
smua.source.output = smua.OUTPUT_OFF

-- define output off state: 2600BS-901-01F_2600B_Reference_Aug2021.pdf - smuX.source.offmode
-- tutorial: https://www.youtube.com/watch?v=Yvyvlwsb4KQ