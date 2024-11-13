package com.br.model;

import java.time.LocalDate;
import java.util.Set;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;

@Entity
public class Conteudo {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long conteudoId;

    @ManyToOne
    @JoinColumn(name = "topico_id")
    private Topico topico;

    private String titulo;

    private String texto;

    private String urlImagem;

    private String videoUrl;

    private LocalDate dataPublicacao;

    @OneToMany(mappedBy = "conteudo")
    private Set<ComentarioConteudo> comentarios;

    @OneToMany(mappedBy = "conteudo")
    private Set<Exercicio> exercicios;

    // Getters e Setters
}
