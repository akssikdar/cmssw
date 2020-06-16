import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *
from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter

_generator = cms.EDFilter("Pythia8GeneratorFilter",
                          
#generator = cms.EDFilter("Pythia8GeneratorFilter",
                         comEnergy = cms.double(13000.0),
                         crossSection = cms.untracked.double(54000000000),
                         filterEfficiency = cms.untracked.double(3.0e-4),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(0),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            user_decay_embedded= cms.vstring(
'#',
'# Particles updated from PDG2018 https://journals.aps.org/prd/abstract/10.1103/PhysRevD.98.030001',
'Particle   pi+         1.3957061e-01   0.0000000e+00',
'Particle   pi-         1.3957061e-01   0.0000000e+00',
'Particle   K_S0        4.9761100e-01   0.0000000e+00',
'Particle   J/psi       3.0969000e+00   9.2900006e-05',
'Particle   Lambda_b0   5.6196000e+00   0.0000000e-04', ## id 5122,
'Particle anti-Lambda_b0 5.6196000e+00   0.0000000e-04',
'#',
'Alias      MyLb        Lambda_b0',
'Alias      Myanti-Lb   anti-Lambda_b0',
'ChargeConj Myanti-Lb   MyLb',
'#',
'Decay MyLb',
'1.000    Lambda0  mu+ mu-  PHOTOS  PHSP;',
'Enddecay',
'CDecay Myanti-Lb',
'End'
), 
            list_forced_decays = cms.vstring('MyLb','Myanti-Lb'),
            operates_on_particles = cms.vint32(),
            convertPythiaCodes = cms.untracked.bool(False)
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),
        PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            "SoftQCD:nonDiffractive = on",
            "5122:m0=5.619600",     ## changing also Lb mass in pythia
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 1.0'),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        )
    )
)

generator = ExternalGeneratorFilter(_generator)
###########
# Filters #
###########

lbfilter = cms.EDFilter("PythiaFilter", ParticleID = cms.untracked.int32(5122))


decayfilter = cms.EDFilter("PythiaDauVFilter", ## signal filter
        verbose         = cms.untracked.int32(0),
        ParticleID      = cms.untracked.int32(5122), 
        NumberDaughters = cms.untracked.int32(3), 
        DaughterIDs     = cms.untracked.vint32(3122, -13, 13),
        MinPt           = cms.untracked.vdouble(0.2, 0.2, 0.2),
        MaxEta          = cms.untracked.vdouble(3.5, 3.0, 3.0),
        MinEta          = cms.untracked.vdouble(-3.5, -3.0, -3.0), 
)
# 

probefilter = cms.EDFilter("PythiaProbeFilter", ## probe filter, use either this or mutagfilter
    verbose         = cms.untracked.int32(1),   ## requires muon with pt>munpt to be not from decay
    NumberOfSisters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(13),
    MomID           = cms.untracked.int32(5122), #Lambda_b0
    SisterIDs       = cms.untracked.vint32(3122,-13), #Lambda0 and mu
    MinPt           = cms.untracked.double(4.), # third Mu with Pt > 4
    MinEta          = cms.untracked.double(-2.5),
    MaxEta          = cms.untracked.double(2.5)
)
# 

# ProductionFilterSequence = cms.Sequence(generator*lbfilter)     
# 
# ProductionFilterSequence = cms.Sequence(generator*lbfilter*decayfilter)     

# ProductionFilterSequence = cms.Sequence(generator*lbfilter*probefilter)     

ProductionFilterSequence = cms.Sequence(generator*lbfilter*decayfilter*probefilter)     
# 
#         MinPt           = cms.untracked.vdouble(0.6, 3.0, 3.0), 
#         MinEta          = cms.untracked.vdouble(-3.0, -3.0, -3.0), 
#         MaxEta          = cms.untracked.vdouble(3.0, 3.0, 3.0)


