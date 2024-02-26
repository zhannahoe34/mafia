import random

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def hello_world(request):
    if request.method == 'GET':
        return render(request, 'home_page.html')
    else:
        form_info = request.POST
        raw_all_players = form_info['players']
        all_players = raw_all_players.split('\r\n')
        
        players_quant = len(all_players)

        killer_roles = 0
        all_roles = 0
        if form_info['werewolf']:
            killer_roles += int(form_info['werewolf'])
            all_roles += int(form_info['werewolf'])
        if form_info['serial_killer']:
            killer_roles += int(form_info['serial_killer'])
            all_roles += int(form_info['serial_killer'])
        if form_info['jester']:
            all_roles += int(form_info['jester'])
        if form_info['sheriff']:
            all_roles += int(form_info['sheriff'])
        if form_info['nurse']:
            all_roles += int(form_info['nurse'])


        if players_quant // 2 < killer_roles:
            return render(request, 'error_need_more_balance.html')
        
        if players_quant < all_roles:
            return render(request, 'error_too_many_roles.html')
        
        random.shuffle(all_players)
        role_dict = {}

        werewolf = int(form_info['werewolf'])
        serial_killer = int(form_info['serial_killer']) if len(form_info['serial_killer']) > 0 else ''
        sheriff = int(form_info['sheriff']) if len(form_info['sheriff']) > 0 else ''
        nurse = int(form_info['nurse']) if len(form_info['nurse']) > 0 else ''
        jester = int(form_info['jester']) if len(form_info['jester']) > 0 else ''

        for player in all_players:
            if werewolf > 0:
                role_dict[player] = 'Werewolf'
                werewolf -= 1
            elif len(form_info['serial_killer']) > 0 and serial_killer > 0:
                role_dict[player] = 'Serial Killer'
                serial_killer -= 1
            elif len(form_info['sheriff']) > 0 and sheriff > 0:
                role_dict[player] = 'Sheriff'
                sheriff -= 1
            elif len(form_info['nurse']) > 0 and nurse > 0:
                role_dict[player] = 'Nurse'
                nurse -= 1
            elif len(form_info['jester']) > 0 and jester > 0:
                role_dict[player] = 'Jester'
                jester -= 1
            else:
                role_dict[player] = 'Townsperson'

        context = {
            'roles': role_dict
        }

        return render(request, 'roles.html', context)