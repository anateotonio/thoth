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
public class Exercicio {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long exercicioId;

    @ManyToOne
    @JoinColumn(name = "conteudo_id")
    private Conteudo conteudo;

    private String descricao;

    private String tipo; // escolha múltipla, verdadeiro/falso, dissertativo

    @OneToMany(mappedBy = "exercicio")
    private Set<RespostaExercicio> respostas;

    // Getters e Setters
}
