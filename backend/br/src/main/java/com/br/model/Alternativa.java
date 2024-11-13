package com.br.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class Alternativa {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long alternativaId;

    @ManyToOne
    @JoinColumn(name = "questao_id")
    private Questao questao;

    private String texto;

    private boolean correta;

    // Getters e Setters
}
