# alias for better default programs
alias ls='exa --group-directories-first --icons --color=auto'
alias lt='exa --tree --icons'

# === COLORES (hex -> truecolor ANSI) ===
# Periwinkle, Dun, Non Photo Blue, Nyanza, Salmon Pink
PERIWINKLE='\[\e[38;2;218;196;247m\]'  # #DAC4F7
DUN='\[\e[38;2;235;210;180m\]'         # #EBD2B4
NP_BLUE='\[\e[38;2;172;236;247m\]'     # #ACECF7
NYANZA='\[\e[38;2;214;246;221m\]'      # #D6F6DD
SALMON='\[\e[38;2;244;152;156m\]'      # #F4989C
RESET='\[\e[0m\]'

# Prompt:
# - usuario@máquina -> periwinkle
# - ruta (\w)       -> dun
# - símbolo $       -> periwinkle
PS1="${PERIWINKLE}\u@\h ${DUN}\w${RESET}\n${PERIWINKLE}\$ ${RESET}"

# Colores para 'ls' (not used, using exa instead)
#alias ls='ls --color=auto'
# Carga paleta base por defecto…
eval "$(dircolors -b)"
# …y sobrescribe lo que nos importa:
# di = directorios      -> Non Photo Blue
# fi = ficheros normales-> Nyanza
# no = texto normal     -> Nyanza (seguro si 'fi' no aplica)
# ex = ejecutables      -> Salmon Pink
LS_COLORS="$LS_COLORS:di=38;2;172;236;247:fi=38;2;214;246;221:no=38;2;214;246;221:ex=38;2;244;152;156"
export LS_COLORS
