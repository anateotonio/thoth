package com.br.model;

import java.time.LocalDate;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class ProgressoUsuario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long progressoId;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;

    @ManyToOne
    @JoinColumn(name = "conteudo_id")
    private Conteudo conteudo;

    private boolean completo;

    private int pontuacao;

    private LocalDate dataConclusao;

    // Getters e Setters
}
