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
public class Topico {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long topicoId;

    @ManyToOne
    @JoinColumn(name = "disciplina_id")
    private Disciplina disciplina;

    private String nome;

    private String descricao;

    @OneToMany(mappedBy = "topico")
    private Set<Conteudo> conteudos;

    @OneToMany(mappedBy = "topico")
    private Set<Questao> questoes;

    // Getters e Setters
}

