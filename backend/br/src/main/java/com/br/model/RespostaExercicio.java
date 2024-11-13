package com.br.model;

import java.time.LocalDate;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class RespostaExercicio {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long respostaId;

    @ManyToOne
    @JoinColumn(name = "exercicio_id")
    private Exercicio exercicio;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;

    private String respostaTexto;

    private LocalDate dataResposta;

    private boolean correta;

    // Getters e Setters
}

