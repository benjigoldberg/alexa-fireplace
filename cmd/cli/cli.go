package server

import (
	"github.com/benjigoldberg/alexa-fireplace/pkg/fireplace"
	"github.com/spf13/cobra"
)

const description = `CLI for controlling the fireplace`

// NewCmd constructs a cobra command for running a spotbot server
func NewCmd(gitSHA string) *cobra.Command {
	f := fireplace.State{}
	cmd := &cobra.Command{
		Use:   "fan",
		Short: description,
		Long:  description,
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := f.Set(); err != nil {
				return err
			}
			return nil
		},
	}

	flags := cmd.Flags()
	flags.BoolVarP(&f.Flame, "flame", "f", false, "Enable flame")
	flags.BoolVarP(&f.BlowerFan, "blower-fan", "b", false, "Enable blower fan")
	return cmd
}
