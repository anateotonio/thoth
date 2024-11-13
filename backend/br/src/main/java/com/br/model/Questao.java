package com.br.model;

import java.util.Set;


import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;

@Entity
public class Questao {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long questaoId;

    @ManyToOne
    @JoinColumn(name = "topico_id")
    private Topico topico;

    private String enunciado;

    private String tipo;

    private String nivelDificuldade;

    @OneToMany(mappedBy = "questao")
    private Set<Alternativa> alternativas;

    // Getters e Setters
}
