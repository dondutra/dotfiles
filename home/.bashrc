# ─────────────────────────────────────────────────────────────────────────────
# dondutra dotfiles — Bash configuration
# yt:    youtube.com/@arkty
# github: github.com/dondutra
# Note: Free to use as long as this header remains, or there is an explicit
#       mention of the creator (dondutra).
# ─────────────────────────────────────────────────────────────────────────────

# -----------------------------------------------------------------------------
# Aliases — sensible defaults (only if the binaries exist)
# -----------------------------------------------------------------------------
if command -v exa >/dev/null 2>&1; then
  alias ls='exa --group-directories-first --icons --color=auto'
  alias lt='exa --tree --icons'
fi

if command -v ccat >/dev/null 2>&1; then
  alias cat='ccat'
fi

# -----------------------------------------------------------------------------
# Prompt colors (hex → truecolor ANSI)
# Palette: Periwinkle, Dun, Non Photo Blue, Nyanza, Salmon Pink
# -----------------------------------------------------------------------------
PERIWINKLE='\[\e[38;2;218;196;247m\]'  # #DAC4F7
DUN='\[\e[38;2;235;210;180m\]'         # #EBD2B4
NP_BLUE='\[\e[38;2;172;236;247m\]'     # #ACECF7
NYANZA='\[\e[38;2;214;246;221m\]'      # #D6F6DD
SALMON='\[\e[38;2;244;152;156m\]'      # #F4989C
RESET='\[\e[0m\]'

# -----------------------------------------------------------------------------
# Prompt
# - user@host → periwinkle
# - path (\w) → dun
# - '$' symbol → periwinkle
# -----------------------------------------------------------------------------
PS1="${PERIWINKLE}\u@\h ${DUN}\w${RESET}\n${PERIWINKLE}\$ ${RESET}"

# -----------------------------------------------------------------------------
# LS_COLORS (kept for compatibility with `ls`; `exa` is used by default)
# -----------------------------------------------------------------------------
# alias ls='ls --color=auto'   # Not used since `exa` is the default

# Load default dircolors palette...
eval "$(dircolors -b)"
# ...and override only what we care about:
# di = directories      → Non Photo Blue
# fi = regular files    → Nyanza
# no = normal text      → Nyanza (safe fallback if 'fi' does not apply)
# ex = executables      → Salmon Pink
LS_COLORS="$LS_COLORS:di=38;2;172;236;247:fi=38;2;214;246;221:no=38;2;214;246;221:ex=38;2;244;152;156"
export LS_COLORS
