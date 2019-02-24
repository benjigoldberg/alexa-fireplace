package fireplace

import (
	"github.com/stianeikeland/go-rpio"
)

const BLOWER_FAN_PIN = 23
const FLAME_PIN = 24

// State represents the state of the fireplace
type State struct {
	Flame     bool `json:"flame"`
	BlowerFan bool `json:"blower_fan"`
}

// Sets both flame and blower fan to enabled setting
func (f State) Set() error {
	if err := setFlame(f.Flame); err != nil {
		return err
	}
	return setBlowerFan(f.BlowerFan)
}

// SetFlame sets the flame state to the given setting
func setFlame(enabled bool) error {
	return setPin(FLAME_PIN, enabled)
}

// SetBlowerFan sets the blower fan state to the given setting
func setBlowerFan(enabled bool) error {
	return setPin(BLOWER_FAN_PIN, enabled)
}

// setPin generically sets a pin on the Raspberry PI
func setPin(pinNumber int, enabled bool) error {
	if err := rpio.Open(); err != nil {
		return err
	}
	defer rpio.Close()

	pin := rpio.Pin(pinNumber)
	pin.Output()
	if enabled {
		pin.High()
	} else {
		pin.Low()
	}
	return nil
}
