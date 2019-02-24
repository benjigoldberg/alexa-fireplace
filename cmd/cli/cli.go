package server

import (
	"github.com/spf13/cobra"
)

const description = `CLI for controlling the fireplace`

// NewCmd constructs a cobra command for running a spotbot server
func NewCmd(gitSHA string) *cobra.Command {
	//c := server.Config{}
	cmd := &cobra.Command{
		Use:   "fan",
		Short: description,
		Long:  description,
		RunE: func(cmd *cobra.Command, args []string) error {
			return nil
		},
	}

	return cmd
}
