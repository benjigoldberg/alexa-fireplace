package server

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"github.com/satori/go.uuid"
	"github.com/spf13/pflag"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
)

type OAuthConfig struct {
	clientID         string
	clientSecret     string
	authorizedEmails []string
}

type OAuth struct {
	config           *oauth2.Config
	authorizedEmails map[string]bool
}

type UserData struct {
	Id            string `json:"id"`
	Email         string `json:"email"`
	VerifiedEmail bool   `json:"verified_email"`
	Name          string `json:"name"`
	GivenName     string `json:"given_name"`
	FamilyName    string `json:"family_name"`
	Picture       string `json:"picture"`
}

func (oc *OAuthConfig) NewOAuth(address string, port int) OAuth {
	config := &oauth2.Config{
		RedirectURL:  fmt.Sprintf("http://%v:%v/oauth/authorize", address, port),
		ClientID:     oc.clientID,
		ClientSecret: oc.clientSecret,
		Scopes:       []string{"https://www.googleapis.com/auth/userinfo.email"},
		Endpoint:     google.Endpoint,
	}
	authorizedEmails := make(map[string]bool, len(oc.authorizedEmails))
	for _, email := range oc.authorizedEmails {
		authorizedEmails[email] = true
	}
	return OAuth{config: config, authorizedEmails: authorizedEmails}
}

// RegisterFlags registers flags with pflag driven CLIs
func (oc *OAuthConfig) RegisterFlags(flags *pflag.FlagSet) {
	flags.StringVar(&oc.clientID, "clientid", "", "Google OAuth Client ID")
	flags.StringVar(&oc.clientSecret, "clientsecret", "", "Google OAuth Client Secret")
	flags.StringSliceVar(&oc.authorizedEmails, "authorized-emails", []string{}, "Authorized Emails")
}

// RegisterMuxes registers HTTP handlers with the webserver mux
func (o *OAuth) RegisterMuxes(mux *http.ServeMux) {
	mux.HandleFunc("/oauth/login", o.loginHandler)
	mux.HandleFunc("/oauth/authorize", o.authHandler)
}

func (o OAuth) loginHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		u, err := uuid.NewV4()
		if err != nil {
			http.Error(w, fmt.Sprintf("Unable to generate UUID: %v", err), http.StatusInternalServerError)
		}
		authURL := o.config.AuthCodeURL(u.String(), oauth2.AccessTypeOffline, oauth2.ApprovalForce)
		http.Redirect(w, r, authURL, http.StatusTemporaryRedirect)
	default:
		http.Error(w, "Method Not Allowed.", http.StatusMethodNotAllowed)
	}
}

func (o OAuth) authHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		code := r.FormValue("code")
		if code == "" {
			http.Error(w, "Failed oauth2 exchange: empty code", http.StatusBadRequest)
			return
		}
		token, err := o.config.Exchange(oauth2.NoContext, code)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed oauth2 exchange: %v", err), http.StatusBadRequest)
			return
		}
		//fmt.Fprintf(w, token.AccessToken)

		userInfoURLTpl := "https://www.googleapis.com/oauth2/v2/userinfo?access_token=%v"
		response, err := http.Get(fmt.Sprintf(userInfoURLTpl, token.AccessToken))
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to fetch user email: %v", err), http.StatusBadRequest)
			return
		}
		defer response.Body.Close()
		user := &UserData{}
		if err = json.NewDecoder(response.Body).Decode(user); err != nil {
			http.Error(w, fmt.Sprintf("Failed to unmarshal JSON: %v", err), http.StatusBadRequest)
			return
		}
		if _, ok := o.authorizedEmails[user.Email]; !ok {
			http.Error(w, fmt.Sprintf("User %v is unauthorized\n", user.Email), http.StatusUnauthorized)
			return
		}
		io.WriteString(w, "Everything went great!")
	default:
		http.Error(w, "Method Not Allowed.", http.StatusMethodNotAllowed)
	}
}
