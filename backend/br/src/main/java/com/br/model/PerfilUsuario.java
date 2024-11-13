package com.br.model;
import java.util.Set;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.OneToOne;

@Entity
public class PerfilUsuario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long perfilId;

    @OneToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;

    private int pontuacaoTotal;
    
    private String nivel;
    
    private String status;

    @ManyToMany
    @JoinTable(
        name = "perfil_badge",
        joinColumns = @JoinColumn(name = "perfil_id"),
        inverseJoinColumns = @JoinColumn(name = "badge_id")
    )
    private Set<Badge> badges;

    // Getters e Setters
}
