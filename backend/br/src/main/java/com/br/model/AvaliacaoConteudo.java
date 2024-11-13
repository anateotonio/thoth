package com.br.model;

import java.time.LocalDate;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class AvaliacaoConteudo {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long avaliacaoId;

    @ManyToOne
    @JoinColumn(name = "conteudo_id")
    private Conteudo conteudo;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;

    private int nota;

    private String comentario;

    private LocalDate dataAvaliacao;

    // Getters e Setters
}
