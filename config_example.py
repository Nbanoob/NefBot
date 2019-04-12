TOKEN = ""
CURRENT_EVENT = ""
PICTURE_SERVER = ""
STREAM_URL = ""
AUTHORIZED_IDs = []
COMMAND_START = "^"
HELP_TEXT = '''
{0}adv - Search for an adventurer by providing the name
	Example usage: {0}adv Euden
{0}wyr - Search for a wyrmprint by providing the name
	Example usage: {0}wyr Glorious Tempest
{0}dra - Search for a dragon by providing the name
	Example usage: {0}dra Midgardsormr
{0}query - Search for an adventurer, dragon, or wyrmprint given select criteria
	Usage: {0}query type=(adv|dra|wyr) element=(Flame|Wind|Water|Light|Shadow) weapon=(Sword|Blade|Dagger|Axe|Lance|Bow|Staff|Wand) skill=(skillname) ability=(abilityname)
	Note that weapon is only applicable to adventurers, and element is only applicable to adventurers and dragons!
	Note that the skill name or ability name must be an exact (case insensitive). Wrap these around quotations
	Example usage: {0}query type=adv element=Flame ability="Stun Res +100%"
{0}update - Updates the bot, fetching the latest data from the configuration file. 
	Note that the database does not get updated with this, it only updates information set in the config file.
{0}exit - Shut down the bot
'''.format(COMMAND_START)
ELEMENT_EMOJI = {"Flame":"<:ele_flame:564111828716748813>", "Wind":"<:ele_wind:564117337431605258>", "Water":"<:ele_water:564117361708367883>", "Light":"<:ele_light:564117313792770084>", "Shadow":"<:ele_shadow:564117273221005318>"}
WEAPON_EMOJI = {"Sword":"<:wep_sword:564117247988334594>", "Blade":"<:wep_blade:564117217726431262>", "Dagger":"<:wep_dagger:564117194141597726>", "Axe":"<:wep_axe:564117173077934090>", "Lance":"<:wep_lance:564117146704019468>", "Bow":"<:wep_bow:564117121169358868>", "Staff":"<:wep_staff:564117050042351625>", "Wand":"<:wep_wand:564117091834396684>"}
UNIT_EMOJI = {"Attack":"<:unit_attack:564116244827996170>", "Defense":"<:unit_defense:564117508747952149>", "Healing":"<:unit_heal:564117544085225482>", "Support":"<:unit_support:564117603895869440>"}
RARITY_EMOJI = {5:"<:rarity_5:564117403861123121>", 4:"<:rarity_4:564117437923065874>", 3:"<:rarity_3:564117463311056947>"}