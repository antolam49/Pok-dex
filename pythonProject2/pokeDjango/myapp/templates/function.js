function myFunction(){
        document.getElementById('HP').style.width = "{{ poke_fr.hp }}%";
        document.getElementById('attack').style.width = "{{ poke_fr.attaque }}%";
        document.getElementById('defense').style.width = "{{ poke_fr.defense }}%";
        document.getElementById('attack_spe').style.width = "{{ poke_fr.attaque_spe }}%";
        document.getElementById('defense_spe').style.width = "{{ poke_fr.defense_spe }}%";
        document.getElementById('speed').style.width = "{{ poke_fr.speed }}%";
    }